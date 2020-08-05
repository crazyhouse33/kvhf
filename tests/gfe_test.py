import kvhf.libs.gfe as gfe
import pytest



def test_simple():
    generator = gfe.explore_commits(gfe.get_repo('test'), reverse=True)
    commit = next(generator)
    path, file= commit.search_files('test')
    assert file.read()==b"test1\n"
    commit = next(generator)
    path,file= commit.search_files('test')
    assert file.read()==b"test2\n"
    commit = next(generator)
    path,file= commit.search_files('test')
    assert file.read()==b"test3\n"

    with pytest.raises(StopIteration):
       commit = next(generator)
        

def test_filter():
    generator= gfe.explore_commits(gfe.get_repo("test"),  filter=["7392e9907a7d1e7e6d77373bd81ff0b992f8ffc3"], reverse=True)
    commit = next(generator)
    path, file= commit.search_files('test')
    assert file.read()==b"test1\n"
    commit = next(generator)
    path,file= commit.search_files('test')
    assert file.read()==b"test3\n"
    with pytest.raises(StopIteration):
        commit = next(generator)



    
        
    
