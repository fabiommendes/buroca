import pathlib
import subprocess
import tempfile
from contextlib import contextmanager

from pyexcel_ods3 import get_data as _get_excel_data

PANDOC_PAIRS = {
    ('markdown', 'latex'),
    ('markdown', 'pdf'),
}
FMT_ALIASES = {
    'md': 'markdown',
}


def convert_file(src, dest, infmt=None, outfmt=None):
    """
    Save file from the given source to the given destination.

    If necessary, it infers file types from the source and destination
    extensions.
    """
    infmt = get_format(src, infmt)
    outfmt = get_format(dest, outfmt)

    if infmt == outfmt:
        copy_file(src, dest)
    elif (infmt, outfmt) == ('markdown', 'pdf'):
        _markdown_to_pdf(src, dest)
    elif (infmt, outfmt) in PANDOC_PAIRS:
        _pandoc_convert(src, dest, (infmt, outfmt))
    else:
        msg = 'cannot convert %s from %s to %s' % (src, infmt, outfmt)
        raise RuntimeError(msg)


def join_pdfs(files, dest):
    """
    Join all input PDF files and save it on the given destination.
    """
    _cli('pdfjam', '-q', '-o', str(dest), '--', *map(str, files))


def get_format(path, fmt=None):
    """
    Return type from path extension.
    """
    if fmt is None:
        fmt = str(path).rpartition('.')[-1]
    fmt = fmt.lower()
    return FMT_ALIASES.get(fmt, fmt)


def copy_file(src, dest):
    """
    Copy file from source to destination.
    """
    with open(src, 'rb') as src_:
        with open(dest, 'wb') as dest_:
            dest_.write(src_.read())


def odt_to_pdf(source, dest):
    """
    Convert .odt file to pdf
    """
    return _libreoffice_headless('-convert-to', 'pdf', source, '-o', dest)


def odt_to_txt(source, dest):
    """
    Convert .odt file to pdf
    """
    return _cli('pandoc', source, '-o', dest)


def read_ods(path):
    """
    Return data from spreadsheet at the given path.
    """
    data = _get_excel_data(str(path))
    if len(data) == 1:
        data, = data.values()
        return data
    return data


@contextmanager
def intermediate_conversion(file_name):
    """
    Realize a intermediate conversion to a file located into a temporary
    path with the given filename.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield pathlib.Path(tmp_dir) / file_name


#
# Auxiliary methods
#
def _cli(*args):
    """
    Execute cli command with the given args.
    """
    return subprocess.run(args, stderr=subprocess.STDOUT)


def _pandoc_convert(src, dest, formats):
    """
    Use pandoc to convert between two file types.
    """
    infmt, outfmt = formats
    _cli('pandoc', str(src), '-o', str(dest), '-r', infmt, '-w', outfmt)


def _libreoffice_headless(*args):
    """
    Execute libreoffice in headless mode
    """
    cmd = ['libreoffice', '-headless']
    subprocess.check_output(cmd)


#
# Specialized converters
#
def _markdown_to_pdf(src, dest):
    _cli('pandoc', '-f', 'markdown', '-t', 'latex', '--pdf-engine', 'xelatex',
         src, '-o', dest)
