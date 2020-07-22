import os
import pytest
import kvhf.kvhfplot.kvhfplot as plot
from kvhf.file import KVH_file


path= '../../kvhf/kvhfplot'
prefix='PYTHONPATH='+path+':../.. python3 '+ path+'/kvhfplot.py '

def selection_keys_t(kvh_file,keys, filter, unity, expected):
    assert plot.select_keys(kvh_file, keys, filter, unity) == expected

    
def selection_pos_t(kvh_file, labels, labels_filter, expected):
    assert plot.select_pos(kvh_file, labels, labels_filter)==expected

def dont_crash(command_line):
    assert os.system(command_line)==0


def test_crash():
    dont_crash( prefix + 'test_data123.hdf test_data145.hdf')
    dont_crash( prefix+ 'test_data123.hdf test_data145.hdf -u tatata')
    dont_crash( prefix+ 'test_data123.hdf test_data145.hdf -u tatata -l commit1 -l commit2 -L commit2')
    dont_crash(prefix+  'test_data123.hdf test_data145.hdf -u tatata -l commit1 -l commit2 -L commit2 -k "loading time"')
    dont_crash(prefix+  'example.hdf -o ../../images/hist.svg')
    dont_crash(prefix+  'example.hdf -l t1 -o ../../images/hist_pie.svg')

    assert os.path.isfile('../../images/hist_pie.svg')
    assert os.path.isfile('../../images/hist.svg')


def test_keys():
    histo1= KVH_file("test_data123.hdf")
    keys=['loading time', 'parsing args']
    filte=['loading time']
    selection_keys_t(histo1, keys, filte,[], ["parsing args"])
    selection_keys_t(histo1, keys, filte,["tata"], [])

    histo2= KVH_file("test_all_print.hdf")
    keys=[]
    filte=[]
    selection_keys_t(histo2, keys, filte,["tata"], [])
    selection_keys_t(histo2, keys, filte,["Mo"], ["executable size"])

    selection_keys_t(histo2, keys, filte,[], ["loading time", "executable size", "parsing args"])




    

