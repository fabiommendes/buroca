import os
import pathlib

import pytest


@pytest.fixture
def examples():
    dirname = os.path.dirname(__file__)
    return pathlib.Path(dirname) / 'examples'
