import os
import pathlib

import click

from .paths import name_for, as_report_path, init as path_init
from .templates import save_rendered_for, save_rendered_all
from .viewers import launch_document_viewer


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
@click.option('--view', '-v', is_flag=True,
              help='launch document viewer afterwards')
def create(template, type, view=False, **kwargs):
    """
    create reports from resources and templates.
    """

    for_ = kwargs.get('for')
    template = normalize_template_path(template)

    if for_ is not None:
        create_for(for_, template, type, view)
    else:
        if view:
            msg = 'Cannot open viewer when generating multiple files.'
            raise SystemExit(msg)
        create_sequence(template, type)


def create_for(for_, template, type, view):
    """
    Implements the "buroca create" command with a --for option.
    """
    template_path = template.absolute()
    dest = name_for(as_report_path(template_path), for_, type)
    save_rendered_for(template_path, dest, for_, type=type)
    if view:
        launch_document_viewer(dest)


def create_sequence(template, type):
    """
    Generate multiple files for the "buroca create" command.
    """
    template_path = template.absolute()
    save_rendered_all(template_path, type=type)


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
