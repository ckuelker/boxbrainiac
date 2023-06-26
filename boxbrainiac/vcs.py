# file: boxbrainiac/vcs.py
import os
from git import Repo, GitCommandError
from boxbrainiac.debug import logger
from boxbrainiac.error import error_message
from boxbrainiac.exception import GitOperationError

def is_git_repo(cfg):
    try:
        r = Repo(cfg['repo_dir'])
        logger.debug(" - Directory is a git repository")
        return True
    except GitCommandError:
        logger.debug(" - Directory is NOT a git repository")
        return False

def git_pull(cfg):
    if is_git_repo(cfg):
        logger.debug(" - Is git repository")
        try:
            logger.debug(" - Git pull")
            repo = Repo(cfg['repo_dir'])
            origin = repo.remotes.origin
            origin.pull()
        except Exception as e:
            raise GitOperationError('GIT-004', str(e))

def git_commit_and_push(cfg, commit_message):
    if is_git_repo(cfg):
        logger.debug(" - Is git repository")
        try:
            yaml_file_path = os.path.join(cfg['repo_dir'], cfg['yaml_file'])
            repo = Repo(cfg['repo_dir'])
            print(str(repo.untracked_files))
            if cfg['yaml_file'] in repo.untracked_files:  
                repo.index.add([cfg['yaml_file']])
                repo.index.commit("Added %s" % cfg['yaml_file'])
                logger.debug(" - Added new file: %s" % cfg['yaml_file'])
            else:
                logger.debug(" - File already tracked:: %s" % cfg['yaml_file'])
            if repo.is_dirty(path=cfg['yaml_file']):
                repo.index.add([cfg['yaml_file']])
                repo.index.commit(commit_message)
                logger.debug(" - Committed changes for: %s" % cfg['yaml_file'])
            else:
                logger.debug(" - Nothing to commit for: %s" % cfg['yaml_file'])
            origin = repo.remotes.origin
            origin.push()
            logger.debug(" - Pushed changes")
        except Exception as e:
            raise GitOperationError('GIT-005', str(e))

