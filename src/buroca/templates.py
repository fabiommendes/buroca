import jinja2


def load_template(path):
    """
    Load template from path.
    """
    
    with open(path) as F:
        return jinja2.Template(F.read())