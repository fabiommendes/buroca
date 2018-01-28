import os
from pathlib import Path

import jinja2

from . import db
from .convert import intermediate_conversion, convert_file
from .errors import TemplateError
from .filters import FILTERS
from .global_functions import GLOBALS
from .paths import name_for, as_report_path


def save_rendered_for(template_path, dest, for_, type=None, base=None):
    """
    Save rendered template for the given entity.

    Args:
        template_path (path):
            Template path
        dest (path):
            Path for the destination file.
        for_:
            Entity name.
        base (path):
            Optional base path for the project's files. If not given, uses CWD.
    """
    ext = os.path.splitext(template_path)[-1]
    namespace = db.load_for(for_, base=base)

    if ext in ['.ods', '.odt']:
        raise NotImplementedError
    else:
        template = load_jinja_template(template_path)
        save_rendered_template(template, namespace, dest, type=type)


def save_rendered_all(template_path, dest=None, type=None, base=None):
    """
    Save rendered templates for multiple entities.

    Args:
        template_path (path):
            The source template path.
        dest (callable):
            A function that receives an entity name and returns the
            corresponding destination path.
        base (path):
            Optional base path for the project's files. If not given, uses CWD.
    """
    ext = os.path.splitext(template_path)[-1]
    namespaces = db.load_all(base=base)
    reports_path = as_report_path(template_path)

    if dest is None:
        dest = (lambda x: name_for(reports_path, x, type))

    if ext in ['.ods', '.odt']:
        raise NotImplementedError
    else:
        template = load_jinja_template(template_path)
        n_items = len(namespaces)
        for idx, (name, namespace) in enumerate(namespaces.items(), 1):
            print('(%s/%s) creating document for "%s".' % (idx, n_items, name))
            save_rendered_template(template, namespace, dest(name), type=type)


def save_rendered_template(template, namespace, dest, type=None):
    """
    Save rendered template to the given destination.

    Args:
        tempalte:
            A Jinja Template instance.
        namespace:
            A namespace mapping to be passed to the Jinja template.
        dest:
            The destination file for the resulting file.
    """
    if type is not None:
        tmp_name = template.path.parts[-1]
        with intermediate_conversion(tmp_name) as tmp:
            save_rendered_template(template, namespace, tmp)
            convert_file(tmp, dest)
    else:
        try:
            data = template.render(namespace)
        except Exception as ex:
            msg = 'Error when rendering %r (%s): %s'
            msg = msg % (dest, type(ex).__name__, ex)
            raise TemplateError(msg)
        with open(dest, 'w') as F:
            F.write(data)


def load_jinja_template(path):
    """
    Load template from path.
    """
    template_path = Path(path)
    ext = os.path.splitext(template_path)[-1].lstrip('.')
    with template_path.open() as F:
        jinja_template = as_template(F.read(), ext)
    jinja_template.path = template_path
    return jinja_template


def as_template(data, type='text'):
    """
    Return a Jinja2 template from the given template string.
    """
    env = jinja2.Environment()
    env.filters.update(FILTERS)
    env.globals.update(GLOBALS)
    return env.from_string(data)
