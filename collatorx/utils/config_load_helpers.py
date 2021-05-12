#
# The following utility tools were obtained from the 
# following repository:
#
# https://github.com/PSPC-SPAC-buyandsell/von-x
#
# Copyright 2017-2018 Government of Canada
# Public Services and Procurement Canada - buyandsell.gc.ca
#

import logging
import os
import re
import pkg_resources
import yaml

from typing import Callable, Mapping, TextIO

DEFAULT_CONFIG_PATH='collatorx:config:settings-test.yml'

def load_resource(path: str) -> TextIO:

    components = path.rsplit(':', 1)
    if len(components) == 1:
        return open(components[0])
    return pkg_resources.resource_stream(components[0], components[1])


def load_settings(env=True) -> dict:

    if env is True:
        env = os.environ
    elif not env:
        env = {}
    env_name = os.environ.get('ENVIRONMENT', 'default')

    settings = {}

    # Load default settings
    with load_resource(DEFAULT_CONFIG_PATH) as resource:
        cfg = yaml.load(resource)
        if 'default' not in cfg:
            raise ValueError('Default settings not found in settings.yml')
        settings.update(cfg['default'])
        if env_name != 'default' and env_name in cfg:
            settings.update(cfg[env_name])

    # Inherit environment variables
    for k, v in env.items():
        if v is not None and v != '':
            settings[k] = v

    # Expand variable references
    for k, v in settings.items():
        if isinstance(v, str):
            settings[k] = expand_string_variables(v, settings)

    return settings

def load_config(path: str, env=None):

    try:
        with load_resource(path) as resource:
            cfg = yaml.safe_load(resource)
    except FileNotFoundError:
        return False
    cfg = expand_tree_variables(cfg, env or os.environ)
    return cfg


def expand_string_variables(value, env: Mapping, warn: bool = True):

    if not isinstance(value, str):
        return value
    def _replace_var(matched):
        default = None
        var = matched.group(1)
        if matched.group(2):
            var = matched.group(2)
            default = matched.group(4)
        found = env.get(var)
        if found is None or found == '':
            found = default
        if found is None and warn:
            logging.getLogger(__name__).warning('Configuration variable not defined: %s', var)
            found = ''
        return found
    return re.sub(r'\$(?:(\w+)|\{([^}]*?)(:-([^}]*))?\})', _replace_var, value)


def map_tree(tree, map_fn: Callable):

    if isinstance(tree, Mapping):
        return {key: map_tree(value, map_fn) for (key, value) in tree.items()}
    if isinstance(tree, (list, tuple)):
        return [map_tree(value, map_fn) for value in tree]
    return map_fn(tree)


def expand_tree_variables(tree, env: Mapping, warn: bool = True):

    return map_tree(tree, lambda val: expand_string_variables(val, env, warn))
