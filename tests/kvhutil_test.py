
import os
import pytest
from kvhf.file import KVH_file


path = '../../kvhf/bin/kvhfutils'
prefix = 'PYTHONPATH=' + path + ':../.. python3 ' + path + '/kvhfutils '


def remove(path):
    try:
        os.remove(path)
    except BaseException:
        pass


# should be dont fail
def dont_crash(command_line):
    assert os.WEXITSTATUS(os.system(command_line)) == 0


def crash(command_line):
    assert os.WEXITSTATUS(os.system(command_line)) != 0


def test_merge():
    remove("merge_out.hkvf")
    dont_crash(
        prefix +
        ' test_data145.hdf test_data123.hdf -m -o merge_out.hkvf')
    expected = KVH_file("concatenation.hdf")
    assert expected == KVH_file("merge_out.hkvf")

    dont_crash(
        prefix +
        '  test_data123.hdf test_data145.hdf -e -o merge_out.hkvf')
    expected = KVH_file('horizontal_concat.hdf')
    assert expected == KVH_file("merge_out.hkvf")


def test_add():
    remove("add_test.hdf")
    dont_crash(
        prefix +
        ' add_test.hdf -k toto:18,18,45 toto:mins:48,48,89 toto:maxs:18,45,63 -k toto:stdevs:45,45,45')

    f = KVH_file('add_test.hdf')
    assert f.dico["toto"].means == [18, 18, 45]
    assert f.dico["toto"].mins == [48, 48, 89]
    assert f.dico["toto"].maxs == [18, 45, 63]
    assert f.dico["toto"].stdevs == [45, 45, 45]
    dont_crash(prefix + 'add_test.hdf -k tata:18,18,45')

    f = KVH_file('add_test.hdf')
    assert f.dico["tata"].means == [18, 18, 45]

    dont_crash(prefix + " add_test.hdf -k exe_size:366 -k exe_size:unity:Ko")


def test_actualized():
    dont_crash(prefix + 'test_new/test -a')
    dont_crash(prefix + 'test_actualized/test -a ')

    crash(prefix + 'test_not_actualized/test.hdf -a ')
    crash(prefix + 'test_not_actualized/test.hdf test_actualized -a ')


def test_extract():
    remove("extract_test.kvhf")
    dont_crash(prefix + ' -o extract_test.kvhf extract_test/test -g')
    f = KVH_file("extract_test.kvhf")
    assert f.labels == ['label1', 'label2', 'label3', 'label4']

    dont_crash(prefix + ' -o extract_test.kvhf extract_test/test -g -d')
    f = KVH_file("extract_test.kvhf")
    assert f.labels == ['label1', 'label2', 'label3', 'label4', 'label5']

    dont_crash(prefix + ' -o extract_test.kvhf -g extract_test/test -C 73b8')
    f = KVH_file("extract_test.kvhf")
    assert f.labels == ['label1', 'label3', 'label4']

    dont_crash(
        prefix +
        ' -o extract_test.kvhf -g extract_test/test -C 73b8 -d')
    f = KVH_file("extract_test.kvhf")
    assert f.labels == ['label1', 'label3', 'label4', 'label5']

    dont_crash(prefix + ' -o extract_test.kvhf -g extract_test/test -c 73b8')
    f = KVH_file("extract_test.kvhf")
    assert f.labels == ['label2']

    dont_crash(
        prefix +
        ' -o extract_test.kvhf -g extract_test/test -c 73b8 b12f')
    f = KVH_file("extract_test.kvhf")
    assert f.labels == ['label2', 'label3', 'label4']

    dont_crash(
        prefix +
        ' -o extract_test.kvhf -g extract_test/test -c 73b8 b12f -C 73b8')
    f = KVH_file("extract_test.kvhf")
    assert f.labels == ['label3', 'label4']

    dont_crash(prefix + ' -o extract_test.kvhf -g test_new/test -d')
    f = KVH_file("extract_test.kvhf")
    assert f.labels == ['labe1']

    dont_crash(prefix + ' -o extract_test.kvhf -g test_new/test ')
    f = KVH_file("extract_test.kvhf")
    assert f.labels == []


def test_disapparing_apparing():

    dont_crash(
        prefix +
        ' -o extract_test.kvhf -g test_apparing_disapparing/test.hdf ')
    f = KVH_file("extract_test.kvhf")
    assert f.labels == ['1', '2', '3']
    assert f.dico['key1'].means == [1.0, 1.0, 1.0]
    assert f.dico['key2'].means == [2.0, None, 4]
    assert f.dico['key3'].means == [None, 3, None]

    dont_crash(
        prefix +
        ' -o extract_test.kvhf -g test_apparing_disapparing/test.hdf --allow-gone-key --check-file')
    f = KVH_file("extract_test.kvhf")
    assert f.labels == ['1', '2', '3']
    assert f.dico['key1'].means == [1.0, 1.0, 1.0]
    assert f.dico['key2'].means == [2.0, None, 4]
    assert f.dico['key3'].means == [None, 3, None]
