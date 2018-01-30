import pytest

from buroca.cli import create
from buroca.convert import convert_file
from tests.conftest import simple_example, get_data

path = simple_example


@pytest.mark.usefixtures('path', 'no_sys_exit')
class TestCliSimpleExample:
    def test_create_for_entity(self):
        result = "John is Beatles's singer."

        # Explicit templates folder
        create.main(['templates/phrase.md', '--for', 'john'])
        assert get_data('reports/phrase-john.md') == result

        # Implicit templates folder
        create.main(['phrase.md', '--for', 'john'])
        assert get_data('reports/phrase-john.md') == result

        # Convert to pdf
        html_result = "<p>John is Beatles’s singer.</p>\n"
        create.main(['phrase.md', '--for', 'john', '-t', 'html'])
        assert get_data('reports/phrase-john.html') == html_result

        # Omit extension
        # create.main(['phrase', '--for', 'john'])
        # assert get_data('reports/phrase-john.md') == result

    def test_create_pdf(self):
        pass