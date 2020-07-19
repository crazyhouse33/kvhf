import git
import os
from collections.abc import Iterable
from types import MethodType

#we add a convenient method to gitpython commit 
def search_files(self, paths):
    if type(paths) == str:#manage mono path
        return (self.tree/os.path.relpath(paths,start=self.repo.working_dir)).data_stream 
    #git python force to use path relative to repo
    return [(self.tree/os.path.relpath(path,start=self.repo.working_dir)).data_stream for path in paths]


git.objects.Commit.search_files =search_files


#filter is integrated in new git rev version, but not in my current so the function handle the commit filter stuff
def git_explore_commits(repo_path, paths_restriction=[], branchs=None, commits=None, filter=[], **kwargs):
    """Generator containing commits matching your selections. Branch is a space separated list of branch. current branch by default. Path restriction come from gitpython that mysteriously decided to not put it in kwarg. Kwargs is argument you can give to the git rev-list command, such as reversed=True, filter=[], skip=5, after...
    """
    repo = git.Repo(repo_path, search_parent_directories=True)
    root= repo.working_dir
    paths= [os.path.relpath(path, start = root) for path in paths_restriction]
    if commits == None:
        commits=[commit for commit in repo.iter_commits(paths=paths_restriction,rev=branchs, **kwargs) if commit.hexsha not in filter]
    else:
        commits=[repo.rev_parse(commit,rev=branchs) for commit in commits if commit not in filter]
    for commit in commits:
        yield commit

def git_get_head(path):
    """Return head of current repo of given path"""
    repo = git.Repo(repo_path, search_parent_directories=True)
    return repo.head




