import os
import pytest
from kvhf.file import KVH_file


path= '../../bin/kvhfutils'
prefix='PYTHONPATH='+path+':../.. python3 '+ path+'/kvhfutils.py '

def remove(path):
    try:
        os.remove(path)
    except:
        pass


#should be dont fail
def dont_crash(command_line):
    assert os.system(command_line)==0

def crash(command_line):
    assert os.system(command_line)!=0

def test_merge():
    remove("merge_out.hkvf")
    dont_crash(prefix + ' test_data145.hdf test_data123.hdf -m -o merge_out.hkvf')
    expected = KVH_file("concatenation.hdf")
    assert expected == KVH_file("merge_out.hkvf")

    dont_crash(prefix + ' test_data145.hdf test_data123.hdf -e -o merge_out.hkvf')
    expected=KVH_file('horizontal_concat.hdf')
    assert expected == KVH_file("merge_out.hkvf")


def test_add():
    remove("add_test.hdf")
    dont_crash( prefix + ' add_test.hdf -k toto:18,18,45 toto:mins:48,48,89 toto:maxs:18,45,63 -k toto:stdevs:45,45,45', )

    f=KVH_file('add_test.hdf')
    assert f.dico["toto"].means==[18,18,45]
    assert f.dico["toto"].mins==[48,48,89]
    assert f.dico["toto"].maxs==[18,45,63]
    assert f.dico["toto"].stdevs==[45,45,45]
    dont_crash( prefix + 'add_test.hdf -k tata:18,18,45' )

    f=KVH_file('add_test.hdf')
    assert f.dico["tata"].means==[18,18,45]

def test_actualized():
    crash(prefix + 'test_not_actualized/test -a')
    crash(prefix + 'test_not_actualized/test test_actualized -a')
    dont_crash(prefix  + 'test_actualized/test -a')
    dont_crash(prefix  + 'test_new/test -a')
    
def test_extract():
    remove("extract_test.kvhf")
    dont_crash( prefix + ' -o extract_test.kvhf extract_test/test -g ' )
    f= KVH_file("extract_test.kvhf")
    assert f.labels== ['label1','label2','label3','label4']

    dont_crash( prefix + ' -o extract_test.kvhf extract_test/test -g -d' )
    f= KVH_file("extract_test.kvhf")
    assert f.labels== ['label1','label2','label3','label4', 'label5']

    dont_crash( prefix + ' -o extract_test.kvhf -g extract_test/test -C ff56'  )
    f= KVH_file("extract_test.kvhf")
    assert f.labels== ['label1','label3','label4']

    dont_crash( prefix + ' -o extract_test.kvhf -g extract_test/test -C ff56 -d'  )
    f= KVH_file("extract_test.kvhf")
    assert f.labels== ['label1','label3','label4','label5']

    dont_crash( prefix + ' -o extract_test.kvhf -g extract_test/test -c ff56'   )
    f= KVH_file("extract_test.kvhf")
    assert f.labels== ['label2']

    dont_crash( prefix + ' -o extract_test.kvhf -g extract_test/test -c ff56 913f8'  )
    f= KVH_file("extract_test.kvhf")
    assert f.labels== ['label2','label3','label4']

    dont_crash( prefix + ' -o extract_test.kvhf -g extract_test/test -c ff56 913f8 -C ff56'  )
    f= KVH_file("extract_test.kvhf")
    assert f.labels== ['label3','label4']

    dont_crash( prefix + ' -o extract_test.kvhf -g test_new/test -d'  )
    f= KVH_file("extract_test.kvhf")
    assert f.labels== ['labe1']

    dont_crash( prefix + ' -o extract_test.kvhf -g test_new/test '  )
    f= KVH_file("extract_test.kvhf")
    assert f.labels== []

















    

