import kvhf.libs.ppath as ppath
import pytest


def test_existing():
    assert ppath.existing_part('tafsqgdsgf') == ''
    assert ppath.existing_part('') == ''
    assert ppath.existing_part('test_gfe') == 'test_gfe'
    assert ppath.existing_part('test_gfe/tafqssdf') == 'test_gfe'
