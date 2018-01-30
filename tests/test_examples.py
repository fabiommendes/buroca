import pytest

from buroca.db import load_for, load_all
from buroca.templates import save_rendered_for
from tests.conftest import simple_example

path = simple_example


@pytest.mark.usefixtures('path')
class TestSimpleExample:
    def test_load_simple_data_for_entity(self):
        beatles = dict(name='Beatles')
        assert load_for('john') == {
            'band': beatles,
            'person': dict(name='John', role='singer')
        }
        assert load_for('ringo') == {
            'band': beatles,
            'person': dict(name='Ringo', role='drummer')
        }

    def test_load_simple_data_all(self):
        beatles = dict(name='Beatles')
        assert load_all() == {
            'john': {
                'band': beatles,
                'person': dict(name='John', role='singer'),
            },
            'paul': {
                'band': beatles,
                'person': dict(name='Paul', role='bass player'),
            },
            'george': {
                'band': beatles,
                'person': dict(name='George', role='guitar player'),
            },
            'ringo': {
                'band': beatles,
                'person': dict(name='Ringo', role='drummer'),
            },
        }

    def test_render_template_for_entity(self):
        save_rendered_for('templates/phrase.md', 'result.md', 'john')
        with open('result.md') as F:
            assert F.read() == "John is Beatles's singer."
