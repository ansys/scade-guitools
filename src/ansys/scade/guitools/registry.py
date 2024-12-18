# -*- coding: utf-8 -*-

# Copyright (C) 2021 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Access to SCADE Studio registry files."""

from collections import namedtuple
from configparser import DEFAULTSECT, RawConfigParser
from typing import Dict

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    # Python 3.7 and earlier
    import importlib_metadata
import os
from pathlib import Path

from ansys.scade.apitools.info import get_scade_version

# each entry is a key
# {
#   'attributes': { <name>: <value> },
#   'keys': { ...}
# }


Key = namedtuple('Key', ['attributes', 'keys'])
"""
"""

_registry = Key({}, {})


def _get_studio_version():
    version = 'v%d' % get_scade_version()
    return version


def _registry_files(version: str):
    path = Path(os.path.expandvars('%APPDATA%/SCADE/Customize'))
    yield from path.glob('*.srg')
    path /= version
    yield from path.glob('*.srg')

    group = 'ansys.scade.registry'
    yield from [_.load()() for _ in importlib_metadata.entry_points(group=group) if _.name == 'srg']


def get_key(path: str) -> Key:
    """
    Return a key from its path.

    Parameters
    ----------
    path : str
        Path of the key.

        For example: ``'Studio/Work Interfaces'``

    Returns
    -------
    Key
        Tuple of attributes and sub-keys as dictionaries.

        For example: ``({}, {'GUIHOST2': ({'pathname': 'ETCUST.DLL', 'version': '24200'}, {}))``
    """
    key = _registry
    for element in path.split('/'):
        key = key.keys.setdefault(element, Key({}, {}))
    return key


def get_key_attributes(path: str) -> Dict[str, str]:
    """
    Return the key's attributes from its path.

    Parameters
    ----------
    path : str
        Path of the key.

        For example: ``'Studio/Work Interfaces/GUIHOST2'``

    Returns
    -------
    Dict[str, str]
        Attributes as a dictionary.

        For example: ``{'pathname': 'ETCUST.DLL', 'version': '24200'}``
    """
    return get_key(path).attributes


def _load_registry(version: str):
    parser = RawConfigParser()
    parser.read(_registry_files(version))
    for section, pairs in parser.items():
        if section == DEFAULTSECT:
            continue
        key = get_key(section)
        key.attributes.update({name.strip('"'): value.strip('"') for name, value in pairs.items()})


# automatic loading of the registry at startup
_load_registry(_get_studio_version())
