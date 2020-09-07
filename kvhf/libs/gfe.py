import git
import os
from collections.abc import Iterable
from types import MethodType

# This is my wrapper around gitpython, which alone is hard to use

# we add a convenient method to gitpython commit


def search_files(self, paths):
    """Search a file relative to cwd in commit"""
    if isinstance(paths, str):  # manage mono path
        return paths, (self.tree / os.path.relpath(paths,
                                                   start=self.repo.working_dir)).data_stream
    # git python force to use path relative to repo
    return [(path, (self.tree / os.path.relpath(path,
                                                start=self.repo.working_dir)).data_stream) for path in paths]


git.objects.Commit.search_files = search_files
Tree = git.objects.tree.Tree


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
    return git.Repo(path, search_parent_directories=True)


def diffs(paths, repo=None):
    """Return diffs with given tree and working_dir. """
    if repo is None:
        repo = git_get_repo(path)
    paths = [os.path.relpath(path, start=repo.working_dir) for path in paths]
    try:
        tree = repo.head.commit.tree
    except ValueError:
        return True  # There were no commit so everything is a diff
    return tree.diff(None, paths=paths)
