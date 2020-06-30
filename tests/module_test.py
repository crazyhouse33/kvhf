from kvhf.file import KVH_file
import matplotlib.pyplot as pyplot
import pytest



def test_init():

    histo1= KVH_file("test_data123.hdf")
    with open("test_data123.hdf") as f:
        histo2=KVH_file(f)

    expected= KVH_file()
    expected.labels=["commit 1", "commit 2", "commit 3"]
    expected.dico={
            "loading time": [10,5,6],
            "executable size": [400, 300, 250],
            "parsing args" : [132, 145, 78],
            "computing images" : [15203,15203, 14569]

            }

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
    histo1= KVH_file("test_data123.hdf")
    histo1.plot(keys=[x for x in histo1.dico.keys() if x!="computing images"])
    histo1.pie_plot(keys=[x for x in histo1.dico.keys() if x!="computing images"])



