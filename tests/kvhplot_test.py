import os
import pytest
import kvhf.bin.kvhfplot.selection as plot
from kvhf.file import KVH_file

import sys

path = '../../kvhf/bin/kvhfplot'
prefix = 'PYTHONPATH=' + path + ':../.. python3 ' + \
    path + '/kvhfplot --dont-block '


def selection_keys_t(kvh_file, keys, filter, unity, expected):
    assert sorted(
        plot.select_keys(
            kvh_file,
            keys,
            filter,
            unity)) == sorted(expected)


def selection_pos_t(kvh_file, labels, labels_filter, expected):
    assert sorted(
        plot.select_pos(
            kvh_file,
            labels,
            labels_filter)) == sorted(expected)


def dont_crash(command_line):
    print('\n\nexecuting', command_line, sys.stderr, '\n\n')
    assert os.system(command_line) == 0


def test_keys():
    histo1 = KVH_file("test_data123.hdf")
    keys = ['loading time', 'parsing args']
    filte = ['loading time']
    selection_keys_t(histo1, keys, filte, [], ["parsing args"])
    selection_keys_t(histo1, keys, filte, ["tata"], [])

    histo2 = KVH_file("test_all_print.hdf")
    keys = []
    filte = []
    selection_keys_t(histo2, keys, filte, ["tata"], [])
    selection_keys_t(histo2, keys, filte, ["Mo"], ["executable size"])

    selection_keys_t(
        histo2, keys, filte, [], [
            "loading time", "executable size", "parsing args"])


def test_pos():
    histo1 = KVH_file("test_data123.hdf")
    hist3 = KVH_file("test_data145.hdf")
    histo1.merge_vertical(hist3)
    labels = ['commit 1', 'commit 2']
    filters = ['commit 2']
    selection_pos_t(histo1, labels, filters, [0])


def test_crash():
    dont_crash(prefix + 'test_data123.hdf test_data145.hdf -r 45')
    dont_crash(prefix + 'test_data123.hdf test_data145.hdf -u tatata')
    dont_crash(
        prefix +
        'test_data123.hdf test_data145.hdf -u tatata -l "commit 1" -l "commit 2" -L "commit 2"')
    dont_crash(
        prefix +
        'test_data123.hdf test_data145.hdf -u tatata -l commit1 -l "commit 2" -L "commit 2" -k "loading time"')

    im_dir = '../../dev/data/images/'
    dont_crash(prefix + 'example.hdf -f png -o ' + im_dir + 'hist.png')
    dont_crash(
        prefix +
        'example.hdf -f png -l t1 -c -o ' +
        im_dir +
        'hist_pie.png')
    dont_crash(
        prefix +
        'example.hdf -f png -l t1 -o ' +
        im_dir +
        'hist_bars.png')

    assert os.path.isfile(im_dir + 'hist_pie.png')
    assert os.path.isfile(im_dir + 'hist.png')
    assert os.path.isfile(im_dir + 'hist_bars.png')
