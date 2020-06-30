from history_dict_file import History_dict_file
import pytest


def test_init():
    histo1= History_dict_file("test_data123.hdf")
    with open("test_data123") as f:
        histo2=History_dict_file(f)

    expected= History_dict_file()
    expected.labels=["commit 1", "commit 2", "commit 3"]
    expected.dico={
            "loading time": [10,5,6],
            "executable size": [400, 300, 250],
            "parsing args" : [132, 145, 78]
            }

    assert histo1 == histo2 == expected
    

def test_merge_horizontal():
    histo1= History_dict_file("test_data123.hdf")
    histo2=  History_dict_file("test_data145.hdf")
    histo1.merge_horizontal(dico2)

    expected= History_dict_file("horizontal_concat.hdf")

    assert expected == histo1

def test_merge_vertical():
    histo1= History_dict_file("test_data123.hdf")
    histo2=  History_dict_file("test_data145.hdf")
    histo1.merge_vertical(dico2)

    expected= History_dict_file("concatenation.hdf")
    assert expected == histo1

def test_plot():
    histo1= History_dict_file("test_data123.hdf")
    histo1.plot_pie()
    histo1.plot()



