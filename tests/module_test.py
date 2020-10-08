from kvhf.file import KVH_file
from kvhf.history_entry import Serie_stats
from collections import defaultdict
import matplotlib.pyplot as pyplot
import pytest


def test_init():

    histo1 = KVH_file("test_data123.hdf")
    with open("test_data123.hdf") as f:
        histo2 = KVH_file(f)

    expected = KVH_file()
    expected.labels = ["commit 1", "commit 2", "commit 3"]
    expected.dico = defaultdict(Serie_stats)
    expected.dico["loading time"].means = [10.0, 5.0, 6.0]
    expected.dico["executable size"].means = [400.0, 300.0, 250.0]
    expected.dico["parsing args"].means = [132.0, 145.0, 78.0]
    expected.dico["computing images"].means = [15203.0, 15203.0, 14569.0]

    assert histo1 == histo2 == expected


def test_merge_horizontal():
    histo1 = KVH_file("test_data123.hdf")
    histo2 = KVH_file("test_data145.hdf")
    histo1.merge_horizontal(histo2)
    expected = KVH_file("horizontal_concat.hdf")

    assert expected == histo1


def test_merge_vertical():
    histo1 = KVH_file("test_data123.hdf")
    histo2 = KVH_file("test_data145.hdf")
    histo1.merge_vertical(histo2)
    expected = KVH_file("concatenation.hdf")
    assert expected == histo1

def test_merge_historic():
    histo1 = KVH_file("test_data123.hdf")
    histo2= KVH_file("test_data123historic.hdf")
    olds, news=histo1.merge_historic(histo2)
    assert sorted(olds) == sorted(["parsing args"])
    assert sorted(news) == sorted(["a_new_key","a_new_key2"])

    expected=KVH_file("test_data123historic_expected.hdf")

    assert expected == histo1




def test_plot():
    histo_full = KVH_file("test_all_print.hdf")
    histo_full.draw_history()

    histo1 = KVH_file("test_data123.hdf")
    histo1.draw_history(
        keys=[x for x in histo1.dico.keys() if x != "computing images"])
    histo1.draw_pie(keys=[x for x in histo1.dico.keys()
                          if x != "computing images"])

    histo2 = KVH_file("one_it.hdf")
    histo2.draw_history()
    histo2.draw_bars()
    histo2.plot(block=False)

    histo3 = KVH_file("test_empty.hdf")
    histo3.draw_history()
    histo3.draw_bars(it=1)
    histo3.draw_pie(it=1)
    histo3.plot(block=False)


def test_dump():
    histo_full = KVH_file("test_all_print.hdf")
    histo_full.dump("test_dump.hdf")
    histo_full2 = KVH_file("test_dump.hdf")
    assert histo_full == histo_full2


def test_empty():
    histo = KVH_file("test_empty.hdf")
    histo.dump("test_empty_out.hdf")
    histo2 = KVH_file("test_empty_out.hdf")
    assert histo2 == histo
    expected = Serie_stats()

    expected.means = [100.0, None, 60.0]
    expected.mins = [60.0, None, 50.0]
    expected.maxs = [150.0, None, 80.0]
    expected.stdevs = [20.0, None, None]
    expected.unity = ''

    assert histo2.dico['loading time'] == expected

    expected2 = Serie_stats()

    expected2.means = [132.0, 145, None]
    expected2.mins = [127, 143, 75.0]
    expected2.maxs = []
    expected2.stdevs = []
    expected2.unity = ''
    assert histo2.dico['parsing args'] == expected2


def test_checks():

    histo3 = KVH_file("not_equilibred.hdf")
    assert histo3.dico['key2'].mins == [1.0]
    keys, biggest, biggest_len = histo3.desequilibred_keys()
    assert sorted(keys) == sorted(['key', 'key3'])
    assert biggest == "key2"
    assert biggest_len == 3

    assert histo3.check_keys()
    assert histo3.check_labels()
    msg, max_key, max_len = histo3.check_alignement()
    assert msg
    assert max_key == 'key2'
    assert max_len == 3

    del histo3.dico['key2']

    assert not histo3.check_keys()
    assert not histo3.check_labels()
    msg, max_key, max_len = histo3.check_alignement()
    assert not msg
    assert max_len == 2

    histo2 = KVH_file("test_empty.hdf")
    assert (not histo2.check_report())


def test_equilibrate():
    histo3 = KVH_file("not_equilibred.hdf")
    max_key, max_len = histo3.get_max_len()
    assert max_key == 'key2'
    assert max_len == 3
    histo3.draw_history(title='tata_tutu')

    histo3.re_equilibrate(['key2'], max_len)
    histo3.re_equilibrate(['key'], max_len, left=True)
    histo3.re_equilibrate(['key3'], max_len, left=False)

    assert histo3.dico['key'].means == [None, 1, 2]
    assert histo3.dico['key2'].means == [1, 2, 3]
    assert histo3.dico['key3'].means == [4, 5, None]
