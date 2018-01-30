import glob
import os
import pathlib
from contextlib import contextmanager

import click


def init(path):
    """
    Create initial folders at the given path.
    """

    abspath = (lambda x: os.path.join(path, x))

    for subpath in ['data', 'reports', 'templates']:
        subpath_ = abspath(subpath)
        if not os.path.exists(subpath_):
            click.echo('creating %r...' % path)
            os.mkdir(subpath_)

    click.echo('Paths successfully created!')


def project_path(*args):
    "Return a subpath into the project's tree"
    return os.path.join(os.getcwd(), *args)


def expand_glob(*args):
    "Expand glob pattern inside the project's directory."

    with workdir(project_path(*args)):
        data = glob.glob(os.path.join(*args))
    return data


@contextmanager
def workdir(path):
    """
    Change cwd to path inside an with block.

    >>> with workdir('some_path'):                            # doctest: + SKIP
    ...     do_something()
    """
    old_path = os.getcwd()

    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_path)


def name_for(template, for_, type=None):
    """
    Convert "template.ext" to "template-for.ext".
    """
    base, new_ext = os.path.splitext(template)
    if type is None:
        ext = new_ext.lstrip('.')
    else:
        ext = EXT_ALIASES.get(type, type)
    return pathlib.Path('%s-%s.%s' % (base, for_, ext))


def as_report_path(path):
    """
    Convert a path at templates/ or data/ to reports
    """
    parts = list(path.parts)
    if parts[-2] not in ['templates', 'data']:
        raise ValueError('invalid template path: %s' % path)
    parts[-2] = 'reports'
    return pathlib.Path(*parts)


def normalize_path(template, required='templates/', glob=False):
    """
    Checks if template path is valid and normalize it to a valid Path object.
    """

    if '/' not in template:
        template = required + template
    elif not template.startswith(required):
        raise SystemExit('path should start with %s' % required)

    path = pathlib.Path(template)
    if not glob and not path.exists():
        raise SystemExit('not found: %s' % template)
    return path


EXT_ALIASES = {
    'markdown': 'md',
    'latex': 'tex',
}