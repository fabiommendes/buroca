import os
from glob import glob as expand_glob

import click

from .convert import join_pdfs
from .paths import name_for, as_report_path, init as path_init
from .paths import normalize_path
from .templates import save_rendered_for, save_rendered_all
from .viewers import launch_document_viewer


@click.group(name='buroca')
def buroca():
    "A small utility for automatic generation of paperwork."


#
# Initialize a buroca project: buroca init
#
@buroca.command()
def init():
    """
    create initial paths.
    """
    path_init(os.getcwd())


#
# Create files: buroca create <template> [...]
#
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
    template = normalize_path(template, 'templates/')

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


#
# Join pdfs: buroca join-pdf [...]
#
@buroca.command('join-pdf')
@click.argument('glob')
@click.option('--view', '-v', is_flag=True,
              help='launch document viewer afterwards')
def join_pdf(glob, view):
    """
    join pdfs from generated reports.
    """
    glob = str(normalize_path(glob, 'reports/', glob=True))
    out_path = glob + '.pdf'
    glob += '-*.pdf'
    files = expand_glob(glob)
    join_pdfs(files, out_path)
    if view:
        launch_document_viewer(out_path)
