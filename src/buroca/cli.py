import click
import os
from . import db, sheets, templates 


@click.group(name='buroca')
def buroca():
    "A small utility for automatic generation of paperwork."


@buroca.command()
def init():
    "create initial paths."

    abspath = (lambda x: os.path.join(curr_path, x))
    curr_path = os.getcwd()

    for path in ['data', 'reports', 'templates']:
        path_ = abspath(path)
        if not os.path.exists(path_):
            click.echo('creating %r...' % path)
            os.mkdir(path_)

    click.echo('Paths successfully created!')


@buroca.command()
@click.argument('template')
@click.argument('resource')
def do(template, resource):
    "create reports from resources and templates."

    template_base, template_ext = os.path.splitext(template)

    # Grab template
    template_path = project_path('templates', template)
    if not os.path.exists(template_path):
        raise SystemExit('template does not exist: %s' % template)
    
    jinja_template = templates.load_template(template_path)
    
    # Load resources
    if resource.endswith('/*'):
        resources = db.find_resources(project_path(), resource[:-2], True)
    else:
        resource_name, entity = resource.split('/')
        resources = {entity: db.load_resources(project_path(), entity, True)}
    
    # Apply template
    for entity, ns in resources.items():
        data = jinja_template.render(ns)
        fname = '%s-%s%s' % (template_base, entity, template_ext)
        
        with open(project_path('reports', fname), 'w') as F:
            F.write(data)
            click.echo('Report: reports/%s.' % fname)


def project_path(*args):
    "Return a subpath into the project's tree"

    return os.path.join(os.getcwd(), *args)
