import os
import pathlib
import tempfile

import click

from .convert import convert_file, get_format
from .paths import name_for, as_report_path, init as path_init
from .templates import save_rendered_for


@click.group(name='buroca')
def buroca():
    "A small utility for automatic generation of paperwork."


@buroca.command()
def init():
    """
    create initial paths.
    """
    path_init(os.getcwd())


@buroca.command()
@click.argument('template')
@click.option('--for', help='select an entity to generate templates to')
@click.option('--type', '-t', help='output format type')
def create(template, type, **kwargs):
    """
    create reports from resources and templates.
    """

    for_ = kwargs.get('for')
    template = normalize_template_path(template)

    if for_ is not None:
        path = template.absolute()
        ext = os.path.splitext(path)[-1]

        with tempfile.TemporaryDirectory() as tmp:
            dest = name_for(as_report_path(path), for_, type)
            if type:
                tmp = pathlib.Path(tmp) / ('temp' + ext)
                save_rendered_for(path, tmp, for_)
                convert_file(tmp, dest, infmt=get_format(path))
            else:
                save_rendered_for(path, dest, for_)

    else:
        raise NotImplementedError


def normalize_template_path(template):
    """
    Checks if template path is valid and normalize it to a valid Path object.
    """

    if '/' not in template:
        template = 'templates/' + template

    path = pathlib.Path(template)
    if not path.exists():
        raise SystemExit('template does not exist at: %s' % template)
    return path
