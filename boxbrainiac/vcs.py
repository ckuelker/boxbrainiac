# file: boxbrainiac/git.py
from dulwich.repo import Repo
from dulwich.porcelain import pull, add, commit, push
from boxbrainiac.debug import logger
from boxbrainiac.error import error_message
from boxbrainiac.exception import GitOperationError

def is_git_repo(cfg):
    try:
        Repo(cfg['repo_dir'])
        logger.debug(" - Directory is a git repository")
        return True
    except Exception:
        logger.debug(" - Directory is NOT a git repository")
        return False

def git_pull(cfg):
    if is_git_repo(cfg):
        try:
            logger.debug(" - Git pull")
            pull(cfg['repo_dir'])
        except Exception as e:
            raise GitOperationError('GIT-003', error_message['GIT-003'], str(e))

def git_commit_and_push(cfg, commit_message):
    if is_git_repo(cfg):
        try:
            repo = Repo(cfg['repo_dir'])
            add(repo, cfg['yaml_file'])
            commit(repo, message=commit_message)
            push(repo, "origin", refspecs="master")
        except Exception as e:
            raise GitOperationError('GIT-004', error_message['GIT-004'], str(e))
