import kvhf.libs.gfe as gfe
import pytest


def test_simple():
    generator = gfe.explore_commits(gfe.get_repo('test'), reverse=True)
    commit = next(generator)
    path, file = commit.search_files('test/test')
    assert file.read() == b"test1\n"
    commit = next(generator)
    path, file = commit.search_files('test/test')
    assert file.read() == b"test2\n"
    commit = next(generator)
    path, file = commit.search_files('test/test')
    assert file.read() == b"test3\n"

    with pytest.raises(StopIteration):
        commit = next(generator)


def test_filter():
    generator = gfe.explore_commits(
        gfe.get_repo("test"),
        filter=["d2558f4f11347a136efe81d4ea97b4c80c4dec14"],
        reverse=True)
    commit = next(generator)
    path, file = commit.search_files('test/test')
    assert file.read() == b"test1\n"
    commit = next(generator)
    path, file = commit.search_files('test/test')
    assert file.read() == b"test3\n"
    with pytest.raises(StopIteration):
        commit = next(generator)
