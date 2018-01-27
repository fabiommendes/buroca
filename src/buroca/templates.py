import os
from pathlib import Path

import jinja2

from . import db
from .filters import FILTERS
from .global_functions import GLOBALS


def save_rendered_for(template, dest, for_, base=None):
    """
    sdfsd
    Args:
        template:
        dest:
        for_:

    Returns:
    """
    ext = os.path.splitext(template)[-1]
    if ext in ['.ods', '.odt']:
        raise NotImplementedError

    else:
        with open(dest, 'w') as F:
            data = render_template_for(template, for_, base=base)
            F.write(data)


def render_template_for(template_path, for_, base=None):
    """
    Render template for the given entity.
    """
    template_path = Path(template_path)
    ext = os.path.splitext(template_path)[-1].lstrip('.')

    with template_path.open() as F:
        jinja_template = as_template(F.read(), ext)
    namespace = db.load_for(for_, base=base)
    return jinja_template.render(namespace)


def load_template(path, type='text'):
    """
    Load template from path.
    """

    with open(path) as F:
        return as_template(F.read(), type)


def as_template(data, type='text'):
    """
    Return a Jinja2 template from the given template string.
    """
    env = jinja2.Environment()
    env.filters.update(FILTERS)
    env.globals.update(GLOBALS)
    return env.from_string(data)
