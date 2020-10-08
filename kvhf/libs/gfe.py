import git
from kvhf.libs.ppath import existing_part
import os
from collections.abc import Iterable
from types import MethodType
from io import BytesIO
from shutil import copyfileobj

# This is my wrapper around gitpython

# we add a convenient method to gitpython commit


def get_stream_cpy(datastream):
    """Take a binary stream like object and return a file like copy with same content, needed because of https://github.com/gitpython-developers/GitPython/issues/1070"""
    res = BytesIO()
    copyfileobj(datastream, res)
    res.seek(0)
    return res


def search_files(self, paths):
    """Search files relative to cwd in commit, return a list of (path,stream)"""
    res = []
    if isinstance(paths, str):
        paths = [paths]
    for path in paths:
        # gitpython only work with path relative to repo
        from_repo_path = os.path.relpath(path, start=self.repo.working_dir)
        # Needed because of
        # https://github.com/gitpython-developers/GitPython/issues/1070

        try:
            datastream = (self.tree / from_repo_path).data_stream
        except KeyError:  # File not existing in the commit
            continue
        res.append((path, get_stream_cpy(datastream)))
    return res


git.objects.Commit.search_files = search_files

# filter is integrated in new git rev version, but not in my current so
# the function handle the commit filter stuff


def explore_commits(repo, paths_restriction=[], branchs=None,
                    commits=None, filter=None, **kwargs):
    """Generator containing commits matching your selections. Branch is a space separated list of branch. current branch by default. Path restriction come from gitpython that mysteriously decided to not put it in kwarg. Kwargs is argument you can give to the git rev-list command, such as reversed=True, filter=[], skip=5, after...
    Filter is a list of begins of hash. Any commit having same begining will be skipped
    """
    if filter is None:
        filter = []

    root = repo.working_dir
    paths = [os.path.relpath(path, start=root) for path in paths_restriction]
    if commits is None:
        try:
            commits = [
                commit for commit in repo.iter_commits(
                    paths=paths_restriction,
                    rev=branchs,
                    **kwargs)]
        except ValueError:  # No commits
            commits = []

    else:
        commits = [repo.rev_parse(commit) for commit in commits]
    for commit in commits:
        if not any(commit.hexsha.startswith(filter_comm)
                   for filter_comm in filter):
            yield commit


def get_repo(path):
    """Return parent git repo"""
    # Gitpython fail if path dont exist in current file system, so we need to
    # give him some existing stuff
    path = existing_part(path)
    return git.Repo(path, search_parent_directories=True)


def diffs(paths, repo):
    """Return diffs with given tree and working_dir. """
    paths = [os.path.relpath(path, start=repo.working_dir) for path in paths]
    try:
        tree = repo.head.commit.tree
    except ValueError:
        return True  # There were no commit so everything is a diff
    return tree.diff(None, paths=paths)
