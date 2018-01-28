"""
Load and locate YAML resources from the /data/ folder of a project.
"""

import os
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace

import yaml


#
# Load YAML resources.
#
def load_for(for_, as_namespace=True, base=None):
    """
    Load all resources for the given entity.

    Args:
        for_ (str):
            Name of the selected entity. It will scan this resource on all
            sub-folders and associate the folder name with folder/<name>.yml in
            the resulting namespace.
        base (str):
            Project directory. Must contain a /data/ folder with yaml files.
        as_namespace (bool):
            If True, return each resource as a SimpleNamespace instance instead
            of a a dictionary.

    Return:
        A dictionary mapping resource names to values.
    """

    base = (Path(base or '.')).absolute()
    datadir = base / 'data'
    ns = {}

    for path in datadir.iterdir():
        if is_resource(path):
            name = path.parts[-1].rpartition('.')[0]
            ns[name] = load_yaml(path)
        elif path.is_dir():
            name = path.parts[-1]
            path = path / (for_ + '.yml')
            ns[name] = load_yaml(path) if path.exists() else None

    if as_namespace:
        for name, value in ns.items():
            if isinstance(name, dict):
                ns[name] = SimpleNamespace(**value)
    return ns


def load_all(reference=None, as_namespace=True, base=None):
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
            result[name] = load_for(name, as_namespace, base)
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


@lru_cache(1024)
def load_yaml(path):
    "Load YAML and return as a simple namespace"
    return yaml.safe_load(open(path))


def is_resource(file):
    "Return True if file extension indicates it is a db resource."
    return str(file).endswith('.yml')
