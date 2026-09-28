import zipfile

import lxml.etree as ET
from lazyutils import lazy
from lxml.etree import XMLSyntaxError

from .convert import _libreoffice_headless
from .templates import as_jinja2_template


class DocTemplate:
    """
    Treat an open document format (.ods, .odt, etc) as a Jinja2 template and
    execute a template transformation.
    """

    xmlns = {
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    }

    zipfile = lazy(lambda self: zipfile.ZipFile(self.path))

    def __init__(self, path):
        self.is_closed = False
        self.path = path

    def _check_open(self):
        if self.is_closed:
            raise RuntimeError('operation cannot be realized on closed file.')

    def xml_tree(self):
        file = self.zipfile.open('content.xml')
        return ET.parse(file)

    def render_template(self, namespace):
        """
        Apply template at content.xml and write back on the zipfile.
        """
        self._check_open()

        xml_root = self.xml_tree().getroot()
        non_rendered = [xml_root.find('office:body', self.xmlns)]

        while non_rendered:
            node = non_rendered.pop()
            node[:] = render_node(node, namespace)

        return ET.tounicode(xml_root)

    def render_at(self, namespace, dest):
        """
        Render template and save result on the given destination.
        """
        self._check_open()
        data = self.render_template(namespace)

        with zipfile.ZipFile(dest, 'w') as zip:
            for file in self.zipfile.namelist():
                if file == 'content.xml':
                    continue
                with zip.open(file, 'w') as dest_file:
                    with self.zipfile.open(file) as src_file:
                        dest_file.write(src_file.read())

            with zip.open('content.xml', 'w') as F:
                F.write(data.encode('utf8'))

    def close(self):
        """
        Close zipfile and flush all data to disk.
        """
        if not self.is_closed:
            self.zipfile.close()
        self.is_closed = True


class CalcTemplate(DocTemplate):
    """
    Process LibreOffice calc templates.
    """

    def render_template(self, namespace):
        """
        Apply template at content.xml and write back on the zipfile.
        """
        self._check_open()

        xml_tree = self.xml_tree()
        xml_root = xml_tree.getroot()
        xmlns = xml_root.nsmap
        cells = xml_root.findall('.//table:table-cell', xmlns)
        for cell in cells:
            cell[:] = render_node(cell, namespace)
        return ET.tounicode(xml_root)


def render_open_doc_template(template, dest, data):
    """
    Open an open office template file and render it on the given destination.

    Args:
        template (str):
            Path to the template file.
        dest:
            Path to the rendered document destination.
        data (dict):
            A namespace of variables that should be applied to the template.

    Returns:
        Nothing
    """
    doc_template = DocTemplate(template)
    doc_template.render_at(data, dest)


def render_node(node, namespace):
    """
    Apply jinja template to etree template Element node.

    Return a transformed Element.
    """

    data = ET.tounicode(node)
    data = data.replace('‘', "'").replace('’', "'")
    rendered = as_jinja2_template(data).render(namespace)
    try:
        result = ET.fromstring(rendered)
        # print('data:', data)
        # print('result:', result)
        return result
    except XMLSyntaxError:
        raise ValueError('cannot create document from template!')


def load_open_document_template(path, type=None):
    """
    Return a template object for a template in the given path.
    """
    if type is None:
        type = str(path).rpartition('.')[-1]
    if type == 'ods':
        return CalcTemplate(path)
    elif type == 'odt':
        return DocTemplate(path)
    else:
        raise ValueError('invalid extension for document: %s' % path)


def launch_calc(fname):
    """
    Launch calc with open socket communication to start communication with
    oosheet.
    """
    return _libreoffice_headless(
        '--calc',
        '--accept="socket,'
        'host=localhost,port=2002;urp;StarOffice.ServiceManager"',
        fname,
    )
