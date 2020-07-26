import os

def prepare_path(path):
    """Create the directories in the path if they dont exist."""
    dir_path = os.path.dirname(os.path.abspath(path))
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path,exist_ok=True)

def open_mkdir(path,*args, **kwarg):
    """Open a file but first create the necessary directories if they dont exist"""
    prepare_path(path)
    return open(path, *args, **kwarg)

