import kvhf.libs.gfe as gfe
import pytest


def test_simple():
    generator = gfe.explore_commits(gfe.get_repo('test_gfe'), reverse=True)
    commit = next(generator)
    path, file = commit.search_files('test_gfe/test')
    assert file.read() == b"test1\n"
    commit = next(generator)
    path, file = commit.search_files('test_gfe/test')
    assert file.read() == b"test2\n"
    commit = next(generator)
    path, file = commit.search_files('test_gfe/test')
    assert file.read() == b"test3\n"

    with pytest.raises(StopIteration):
        commit = next(generator)


def test_filter():
    generator = gfe.explore_commits(
        gfe.get_repo("test_gfe"),
        filter=["01471ef6658ee9a96d1d69f926240edf641c1c20"],
        reverse=True)
    commit = next(generator)
    path, file = commit.search_files('test_gfe/test')
    assert file.read() == b"test1\n"
    commit = next(generator)
    path, file = commit.search_files('test_gfe/test')
    assert file.read() == b"test3\n"
    with pytest.raises(StopIteration):
        commit = next(generator)
