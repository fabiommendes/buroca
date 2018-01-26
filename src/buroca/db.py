"""
Load and locate YAML resources from the /data/ folder of a project.
"""

import os
from types import SimpleNamespace
from functools import lru_cache

import yaml


#
# Load YAML resources.
#
def load_resources(base, name, as_namespace=False):
    """
    Load all resources on the given path.

    Args:
        base (str):
            Project directory. Must contain a /data/ folder with yaml files. 
        name (str):
            Name of the required resource. It will scan this resource on all
            sub-folders and associate the folder name with folder/<name>.yml
            in the resulting namespace.
        as_namespace (bool):
            If True, return each resource as a SimpleNamespace instance instead
            of a a dictionary.

    Return:
        A dictionary mapping resource names to values.
    """

    datadir = os.path.join(base, 'data')
    paths = os.listdir(datadir)
    ns = {}

    for path in paths:
        fullpath = os.path.join(datadir, path)

        if is_resource(path):
            ns[path[:-4]] = load_yaml(fullpath)

        elif os.path.isdir(fullpath):
            resource_path = os.path.join(fullpath, name) + '.yml'
            resource_name = os.path.split(fullpath)[-1]
            data = (load_yaml(resource_path)
                    if os.path.exists(resource_path) else None)
            ns[resource_name] = data

    if as_namespace:
        for name, value in ns.items():
            if isinstance(name, dict):
                ns[name] = SimpleNamespace(**value)
    return ns


def find_resources(base, path_from=None, as_namespace=False):
    """
    Return a mapping of entity to namespace using the given path as reference
    to locate entity values.
    """

    path_from = path_from or locate_entities(base)
    resource_path = os.path.join(base, 'data', path_from)
    files = os.listdir(resource_path)
    names = [f[:-4] for f in files if is_resource(f)]
    return {name: load_resources(base, name, as_namespace) for name in names}


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
    return file.endswith('.yml')
