#!/usr/bin/env python3
# file: boxbrainiac/main.py
import os
import sys

from flask import Flask, request, render_template, redirect, url_for, escape
from fuzzywuzzy import fuzz
import html

from boxbrainiac.config import cfg
from boxbrainiac.debug import logger
import boxbrainiac.env as env
from boxbrainiac.exception import GitOperationError, StoreOperationError, DataProcessingError
import boxbrainiac.git as git
import boxbrainiac.store as store
import boxbrainiac.util as util

def run_app():

    cfg['cwd'] = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    template_folder = os.path.join(cfg['cwd'], cfg['tpl'])
    app = Flask(__name__, template_folder=template_folder)

    (args, is_debug) = env.get(cfg)

    cfg['repo_dir'] = args.repo_dir # $HOME/.boxbrainiac/data
    cfg['yaml_file'] = args.yaml_file # boxbrainiac.yaml
    cfg['yaml_path'] = os.path.join(cfg['repo_dir'],cfg['yaml_file']) # $HOME/.boxbrainiac/data/boxbrainiac.yaml

    @app.errorhandler(DataProcessingError)
    def handle_data_processing_error(error):
        return render_template('error_view.html', number='DAT-006', message=error.message, copyright=cfg['copyright']), 500

    @app.errorhandler(StoreOperationError)
    def handle_store_operation_error(error):
        return render_template('error_view.html', number=error.number, message=error.message, copyright=cfg['copyright']), 500

    @app.errorhandler(GitOperationError)
    def handle_git_operation_error(error):
        return render_template('error_view.html', number=error.number, message=error.message, copyright=cfg['copyright']), 500

    store.ensure_yaml_exists(cfg)

    # Routes related to boxbrainiac (CRUD operations)
    @app.route('/' + cfg['ns'], methods=['POST'])
    def manage_boxes():
        git.git_pull(cfg)  # Pull before writing
        try:
            #realm = html.escape(request.form['realm'])
            #content = html.escape(request.form['content'])
            #location = html.escape(request.form['location'])
            realm = request.form['realm']
            content = request.form['content']
            location =request.form['location']
        except (TypeError, KeyError) as e:
            raise DataProcessingError('DAT-006', str(e))
        data = store.read_yaml(cfg)
        if data['available_ids']:
            new_id = data['available_ids'].pop(0)  # Use the smallest available ID
        else:
            new_id = len(data[cfg['ns']]) + 1

        new_box = {
            'id': new_id,
            'realm': realm,
            'content': content,
            'location': location
        }

        data[cfg['ns']].append(new_box)

        store.write_yaml(cfg,data)
        git.git_commit_and_push(cfg, "Add new entity")  # Commit and push after writing
        return redirect(url_for('list_view'))

    @app.route('/edit/<int:box_id>', methods=['GET', 'POST'])
    def edit_box(box_id):
        git.git_pull(cfg)  # Pull before reading or writing
        data = store.read_yaml(cfg)
        if request.method == 'GET':
            try:
                box = next((box for box in data[cfg['ns']] if box['id'] == box_id), None)
                if not box:
                    return "Entity not found", 404
                sanitized_box = {key: escape(value) for key, value in box.items()}
            except (TypeError, KeyError) as e:
                raise DataProcessingError('DAT-007', str(e))
            return render_template('edit_view.html', box=sanitized_box, copyright=cfg['copyright'])

        elif request.method == 'POST':
            try:
                #realm = html.escape(request.form['realm'])
                #content = html.escape(request.form['content'])
                #location = html.escape(request.form['location'])
                realm = request.form['realm']
                content = request.form['content']
                location =request.form['location']

                box_index = next((index for index, box in enumerate(data[cfg['ns']]) if box['id'] == box_id), None)
                if box_index is None:
                    return "Entity not found", 404

                data[cfg['ns']][box_index]['realm'] = realm
                data[cfg['ns']][box_index]['content'] = content
                data[cfg['ns']][box_index]['location'] = location
            except (TypeError, KeyError) as e:
                raise DataProcessingError('DAT-008', str(e))

            store.write_yaml(cfg, data)
            git.git_commit_and_push(cfg,"Edit entity with ID {}".format(box_id) )  # Commit and push after writing
            return redirect(url_for('list_view'))

    @app.route('/delete/<int:box_id>', methods=['POST'])
    def delete_box(box_id):
        git.git_pull(cfg)  # Pull before reading or writing
        data = store.read_yaml(cfg)
        box_index = util.find_box_index(cfg, data, box_id)
        if box_index is not None:
            try:
                data[cfg['ns']].pop(box_index)
                # Return the deleted box's ID to the available_ids list
                data['available_ids'].append(box_id)
                # Keep the list sorted to easily retrieve the smallest ID
                data['available_ids'].sort()
                store.write_yaml(cfg, data)
                git.git_commit_and_push(cfg, "Delete entity with ID {}".format(box_id))  # Commit and push after writing
            except (TypeError, KeyError) as e:
                raise DataProcessingError('DAT-009', str(e))
        return redirect(url_for('list_view'))

    # Other routes (views and search)
    @app.route('/')
    def index():
        return redirect(url_for('list_view'))

    @app.route('/list')
    def list_view():
        git.git_pull(cfg)  # Pull before reading
        data = store.read_yaml(cfg)

        try:
            # Sort the box list by ID
            sorted_boxes = sorted(data[cfg['ns']], key=lambda box: box['id'])

            # Sanitize the boxes before sending them to the template
            sanitized_boxes = []
            for box in sorted_boxes:
                sanitized_box = {key: escape(value) for key, value in box.items()}
                sanitized_boxes.append(sanitized_box)
        except (TypeError, KeyError) as e:
            raise DataProcessingError('DAT-010', str(e))
        return render_template('list_view.html', boxes=sanitized_boxes, copyright=cfg['copyright'])

    @app.route('/input')
    def input_view():
        return render_template('input_view.html', copyright=cfg['copyright'])

    @app.route('/search', methods=['GET'])
    def search_view():
        search_query = request.args.get('search_query')
        search_results = None

        sanitized_results = []
        if search_query:
            try:
                query = search_query.lower() # Sanitized by Flachs Jinja2
                data = store.read_yaml(cfg)
                search_results = [box for box in data[cfg['ns']] if fuzz.partial_ratio(box['content'].lower(), query) >= 70]

                # Sanitize the search_results, not really needed for Flachs
                # Jinja2, except this gets used in attributes or JavaScript
                # later
                for box in search_results:
                    sanitized_box = {key: escape(value) for key, value in box.items()}
                    sanitized_results.append(sanitized_box)

            except (TypeError, KeyError) as e:
                raise DataProcessingError('DAT-011', str(e))

        return render_template('search_view.html', search_results=sanitized_results, copyright=cfg['copyright'])

    app.run(args.host, port=args.port, debug=is_debug)
    return app

# Main entry point
if __name__ == '__main__':
    #run_app(sys.argv[1:])
    run_app()

