"""
Load and locate YAML resources from the /data/ folder of a project.
"""

import os
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

TYPE_PRIORITY = [
    # Collection formats
    'pickle', 'csv', 'xlsx', 'xls', 'html', 'xml', 'sqlite', 'ini',

    # Individual formats
    'yml', 'json',
]


#
# Load YAML resources.
#
def load_for(for_, base=None):
    """
    Load all resources for the given entity.

    Args:
        for_ (str):
            Name of the selected entity. It will scan this resource on all
            sub-folders and associate the folder name with folder/<name>.yml in
            the resulting namespace.
        base (str):
            Project directory. Must contain a /data/ folder with yaml files.

    Return:
        A dictionary mapping resource names to values.
    """

    get_name = (lambda x: os.path.splitext(x.parts[-1])[0])
    base = (Path(base or '.')).absolute()
    datadir = base / 'data'

    # Collect names
    names = defaultdict(list)
    for path in datadir.iterdir():
        names[get_name(path)].append(path)

    # Create namespace
    ns = {name: resource(paths, for_) for name, paths in names.items()}
    return ns


def path_priority(path):
    """
    Return the priority number for files of the given path.
    Highest numbers are chosen first.
    """
    ext = os.path.splitext(path)[-1].lstrip('.')
    n = len(TYPE_PRIORITY)
    try:
        return n - TYPE_PRIORITY.index(ext)
    except ValueError:
        return 0


def resource(paths, for_):
    """
    Return the resource corresponding to the given group of paths.

    * Files have preference over directories
    * Priority is defined by extension in the order of TYPE_PRIORITY
    """
    if len(paths) == 0:
        return None
    elif len(paths) == 1:
        return resource_from_path(paths[0], for_)
    else:
        return resource_from_path(sorted(paths, key=path_priority)[0], for_)


def resource_from_path(path, for_):
    """
    Fetch resource for the given entity in the specified path.
    """
    ext = os.path.splitext(path)[-1].lstrip('.')

    if path.is_dir():
        path = path / (for_ + '.yml')
        return load_yaml(path) if path.exists() else None
    elif ext == 'yml':
        return load_yaml(path)


def load_all(reference=None, base=None):
    """
    Return a mapping of each entity to namespace using the given path as reference
    to locate entity values.
    """
    base = (Path(base or '.')).absolute()

    # Choose the correct reference
    if reference is None:
        reference = locate_entities(base)
    elif isinstance(reference, str):
        pass

    resource_path = base / 'data' / reference
    result = {}
    for subpath in resource_path.iterdir():
        if is_resource(subpath):
            name = subpath.parts[-1].rpartition('.')[0]
            result[name] = load_for(name, base)
    return result


def locate_entities(base):
    """
    Return a possible reference path for a directory that stores project's
    entities
    """
    datadir = os.path.join(base, 'data')
    paths = (os.path.join(datadir, f) for f in os.listdir(datadir))
    folders = [f for f in paths if os.path.isdir(f)]

    if not folders:
        return None
    elif len(folders) == 1:
        name, = folders
        return os.path.split(name)[-1]
    else:
        files = {f: {f for f in os.listdir(f) if is_resource(f)}
                 for f in folders}
        resource_set = set()
        resource_path = None

        for path, data in files.items():
            if resource_set.issubset(data):
                resource_set = data
                resource_path = path
            elif resource_set.issuperset(data):
                pass
            else:
                msg = 'inconsistent resources: %s and %s'
                raise TypeError(msg % (resource_path, path))

        return resource_path


#
# File loaders
#
LOADER_MAP = {}


def single_loader(ext):
    """
    Register function as a loader for the given file extension.
    """

    def decorator(func):
        LOADER_MAP[ext] = func
        return func

    return decorator


@single_loader('yaml')
@single_loader('yml')
@lru_cache(1024)
def load_yaml(path):
    import yaml
    return yaml.safe_load(open(path))


@single_loader('json')
@lru_cache(1024)
def load_json(path):
    import json
    return json.load(open(path))


def is_resource(file):
    "Return True if file extension indicates it is a db resource."
    return str(file).endswith('.yml')
