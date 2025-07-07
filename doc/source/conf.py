"""Sphinx documentation configuration file."""

from datetime import datetime
import os

from ansys_sphinx_theme import (
    ansys_favicon,
    get_version_match,
)

from ansys.scade.guitools import __version__

# Project information
project = 'ansys-scade-guitools'
copyright = f'(c) {datetime.now().year} ANSYS, Inc. All rights reserved'
author = 'ANSYS, Inc.'
release = version = __version__
switcher_version = get_version_match(version)

# Select desired logo, theme, and declare the html title
html_theme = 'ansys_sphinx_theme'
html_short_title = html_title = 'Ansys SCADE GUI Tools'

# multi-version documentation
cname = os.getenv('DOCUMENTATION_CNAME', 'guitools.scade.docs.pyansys.com')
"""The canonical name of the webpage hosting the documentation."""

# specify the location of your github repo
html_theme_options = {
    'github_url': 'https://github.com/ansys/scade-guitools',
    'show_prev_next': False,
    'show_breadcrumbs': True,
    'additional_breadcrumbs': [
        ('PyAnsys', 'https://docs.pyansys.com/'),
    ],
    'switcher': {
        'json_url': f'https://{cname}/versions.json',
        'version_match': switcher_version,
    },
    'check_switcher': False,
    'logo': 'pyansys',
    'ansys_sphinx_theme_autoapi': {
        'project': project,
        'own_page_level': 'function',
        'class_content': 'both',  # documentation in https://sphinxdocs.ansys.com/version/stable/user-guide/autoapi.html
        'member_order': 'alphabetical',
        'ignore': ['*/src/ansys/scade/guitools/impl/*', '*/src/ansys/scade/guitools/test/*'],
    },
}

# Configuration for Sphinx autoapi
# TODO(Jean Henry): #026 is the issue number
# https://github.com/ansys/scade-guitools/issues/26

# autoapi_render_in_single_page = ["class", "enum", "exception", "function"]

# Sphinx extensions
extensions = [
    'numpydoc',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'sphinx_design',
    'ansys_sphinx_theme.extension.autoapi',
]

# ansys.scade.apitools.prop not found when building the documentation
suppress_warnings = ['autoapi.python_import_resolution']

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.10', None),
}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_xref_param_type = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    'GL06',  # Found unknown section
    'GL07',  # Sections are in the wrong order.
    # TODO(Muhammed Adedigba): activate GL08 once numpydoc v1.9.0 bug is fixed
    # https://github.com/numpy/numpydoc/issues/638
    # https://github.com/ansys/scade-guitools/issues/26
    #'GL08',  # The object does not have a docstring
    'GL09',  # Deprecation warning should precede extended summary
    'GL10',  # reST directives {directives} must be followed by two colons
    'SS01',  # No summary found
    'SS02',  # Summary does not start with a capital letter
    'SS03',  # Summary does not end with a period
    'SS04',  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    'RT02',  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}

# Favicon
html_favicon = ansys_favicon

# static path
html_static_path = ['_static']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# TODO(Jean Henry): remove ignore links after public release
# https://github.com/ansys/scade-guitools/issues/26
linkcheck_ignore = [
    'https://github.com/ansys/scade-guitools',
    'https://github.com/ansys/scade-guitools/actions/workflows/ci_cd.yml',
    'https://pypi.org/project/ansys-scade-guitools',
    # The link below takes a long time to check
    'https://www.ansys.com/products/embedded-software/ansys-scade-suite',
    'https://www.ansys.com/*',
]


if switcher_version != 'dev':
    linkcheck_ignore.append(f'https://github.com/ansys/scade-guitools/releases/tag/v{__version__}')
