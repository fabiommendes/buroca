import os

from buroca.convert import odt_to_txt, read_ods
from buroca.loffice import render_open_doc_template


class TestOpenDocTemplate:
    def test_can_render_open_document_template(self, examples):
        template = examples / 'template.odt'
        result = examples / 'result.odt'
        txt = examples / 'result.txt'

        render_open_doc_template(
            template,
            result,
            {'title': 'First template', 'name': 'world'}
        )
        try:
            odt_to_txt(result, txt)
            assert open(txt).read() == 'First template\n\nHello world!\n'
        finally:
            os.unlink(txt)

    def test_can_render_calc_template(self, examples):
        template = examples / 'template.ods'
        result = examples / 'result.ods'

        render_open_doc_template(
            template,
            result,
            {'name': 'answer', 'value': '42'}
        )

        assert read_ods(result) == [['answer', '42']]
