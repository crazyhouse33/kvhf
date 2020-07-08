import git
import os
#filter is integrated in new git rev version, but not in my current so the function handle the commit filter stuff
def git_file_explore(path, branchs=None, commits=None, filter=[], **kwargs):
    """Generator containing tuples (File, commit) matching your selections. Branch is a space separated list of branch. current branch by default. Kwargs is argument you can give to the git rev-list command, such as reversed=True, filter=[], skip=5, after...
    """
    repo = git.Repo(path, search_parent_directories=True)
    root= repo.working_dir
    path= os.path.relpath(path, start = root)
    if commits == None:
        commits=[commit for commit in repo.iter_commits(paths=path,rev=branchs, **kwargs) if commit.hexsha not in filter]
    else:
        commits=[repo.rev_parse(commit) for commit in commits if commit not in filter]

    for commit in commits:
        file = commit.tree / path 
        yield file.data_stream, commit


