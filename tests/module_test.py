from kvhf.file import KVH_file
from kvhf.stat import Serie_stats 
from collections import defaultdict
import matplotlib.pyplot as pyplot
import pytest



def test_init():

    histo1= KVH_file("test_data123.hdf")
    with open("test_data123.hdf") as f:
        histo2=KVH_file(f)

    expected= KVH_file()
    expected.labels=["commit 1", "commit 2", "commit 3"]
    expected.dico=defaultdict(Serie_stats)
    expected.dico["loading time"].means=[10.0,5.0,6.0]
    expected.dico["executable size"].means=[400.0,300.0,250.0]
    expected.dico["parsing args"].means=[132.0,145.0,78.0]
    expected.dico["computing images"].means=[15203.0,15203.0, 14569.0]

    assert histo1 == histo2 == expected
    

def test_merge_horizontal():
    histo1= KVH_file("test_data123.hdf")
    histo2=  KVH_file("test_data145.hdf")
    histo1.merge_horizontal(histo2)

    expected= KVH_file("horizontal_concat.hdf")

    assert expected == histo1

def test_merge_vertical():
    histo1=  KVH_file("test_data123.hdf")
    histo2=  KVH_file("test_data145.hdf")
    histo1.merge_vertical(histo2)

    expected= KVH_file("concatenation.hdf")
    assert expected == histo1

def test_plot():
    histo_full=KVH_file("test_all_print.hdf")
    histo_full.plot()
    pyplot.show(block=False)

    histo1= KVH_file("test_data123.hdf")
    histo1.plot(keys=[x for x in histo1.dico.keys() if x!="computing images"])
    histo1.pie_plot(keys=[x for x in histo1.dico.keys() if x!="computing images"])



