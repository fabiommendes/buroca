import os
import pathlib
import sys
import tempfile
from contextlib import contextmanager

import mock
import pytest

SIMPLE_BEATLES_DATA = {
    'data/person/john.yml': 'name: John\nrole: singer',
    'data/person/paul.yml': 'name: Paul\nrole: bass player',
    'data/person/george.yml': 'name: George\nrole: guitar player',
    'data/person/ringo.yml': 'name: Ringo\nrole: drummer',
    'data/band.yml': 'name: Beatles',
    'templates/phrase.md':
        '{{person.name}} is {{ band.name }}\'s {{ person.role}}.',
}


@pytest.fixture
def examples():
    dirname = os.path.dirname(__file__)
    return pathlib.Path(dirname) / 'examples'


@pytest.yield_fixture
def temp_dir():
    try:
        with tempfile.TemporaryDirectory() as tmp:
            yield tmp
    finally:
        pass


@pytest.fixture
def tree():
    return tree_maker


@pytest.yield_fixture
def simple_example():
    """
    Simple example inspired on the readme
    """
    with tree_maker(SIMPLE_BEATLES_DATA) as tmp:
        yield tmp


@pytest.yield_fixture
def no_sys_exit():
    exit_function = (lambda *args: None)
    with mock.patch('sys.exit', exit_function):
        yield exit_function


#
# Auxiliary functions
#
@contextmanager
def tree_maker(data):
    old_dir = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp)

        for k, v in data.items():
            subpath = path.joinpath(k)
            if v is None:
                subpath.mkdir()
            else:
                basedir = pathlib.Path(*subpath.parts[:-1])
                basedir.mkdir(parents=True, exist_ok=True)
                with open(subpath, 'w') as F:
                    F.write(v)

        try:
            os.chdir(tmp)
            yield tmp
        finally:
            os.chdir(old_dir)


def get_data(path):
    """
    Return data of file on the given path as a string.
    """
    with open(path) as F:
        return F.read()
