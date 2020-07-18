from gfe.gfe import git_explore_commits
import pytest



def test_simple():
    generator = git_explore_commits("test", reverse=True)
    commit = next(generator)
    file= commit.search_files('test')
    assert file.read()==b"test1\n"
    commit = next(generator)
    file= commit.search_files('test')
    assert file.read()==b"test2\n"
    commit = next(generator)
    file= commit.search_files('test')
    assert file.read()==b"test3\n"

    with pytest.raises(StopIteration):
       commit = next(generator)
        

def test_filter():
    generator= git_explore_commits("test",  filter=["7392e9907a7d1e7e6d77373bd81ff0b992f8ffc3"], reverse=True)
    commit = next(generator)
    file= commit.search_files('test')
    assert file.read()==b"test1\n"
    commit = next(generator)
    file= commit.search_files('test')
    assert file.read()==b"test3\n"
    with pytest.raises(StopIteration):
        commit = next(generator)



    
        
    
