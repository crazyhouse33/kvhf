from lib.done import Done_file
import os
import pytest

Done_file.init_done_repo('.done')
done_file= Done_file()
done_file.set_done(['hey', 'ho','no'])
done_file.save()



    

def test_find():
    old=os.getcwd()
    assert Done_file.find_path() == os.path.abspath('.done')

    os.chdir("test_new")
    assert Done_file.find_path() == old+'/.done'
    assert Done_file.find_path('tot') =='tot' 

    os.chdir(old)

def test_parse():
    with open(".done/done")as f:
        assert list(Done_file._parse(f).keys())==['hey','ho','no']
    with open(".done/lock")as f:
        assert Done_file._parse(f)=={}


def test_are_done():
    assert done_file.done(['azf','heyqsfqsf','hazfsq','no']) == ['no']
    assert done_file.done([])==[]
    assert done_file.done(['azf','heyqsfqsf','hazfsq','noa'])==[]

def test_manips():

    done_file.lock('tat')
    assert done_file.locked()==['tat']
    with pytest.raises(ValueError):
        done_file.set_done(['lolo','no','tat'])
    done_file.set_done('tata')
    assert done_file.done(['tata','hey','ho','no','aaa' ])==['tata','hey','ho','no']
    done_file.undo(['tata', 'hey'])
    assert done_file.done(['tata','hey','ho','no','aaa' ])== ['ho','no']
    assert done_file.done()==['ho','no']

    done_file.save()
    done_file2= Done_file()
    assert done_file2.done()==['ho','no']
    assert done_file2.locked()==['tat']




