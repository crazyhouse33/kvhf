from gfe.gfe import git_file_explore
import pytest



def test_simple():
    generator = git_file_explore("test", reverse=True)
    file, commit = next(generator)
    assert file.read()==b"test1\n"
    file, commit = next(generator)
    assert file.read()==b"test2\n"
    file, commit = next(generator)
    assert file.read()==b"test3\n"

    with pytest.raises(StopIteration):
        file, commit = next(generator)
        

def test_filter():
    generator= git_file_explore("test",  filter=["7392e9907a7d1e7e6d77373bd81ff0b992f8ffc3"], reverse=True)
    file, commit = next(generator)
    assert file.read()==b"test1\n"
    file, commit = next(generator)
    assert file.read()==b"test3\n"
    with pytest.raises(StopIteration):
        file, commit = next(generator)



    
        
    
