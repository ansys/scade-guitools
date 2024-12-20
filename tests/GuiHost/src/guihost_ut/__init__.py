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

"""Provides GuiHost client pages for tests."""

from guihost_ut.test_client import PageAll, PagePython, PageTxt


def pages() -> list:
    r"""
    Return the list of GuiHost client pages.

    This function implements the entry point "ansys.scade.guihost/pages".
    """
    return [PAGE_TXT, PAGE_ALL, PAGE_PY]


# page for text files (TXT)
PAGE_TXT = {
    'version': 24200,
    'expire': 25100,
    'page': 'Misc.',
    'category': 'Text',
    'optional': False,
    'class': PageTxt,
}

# page for all files (*)
PAGE_ALL = {
    'version': 24200,
    'expire': 25100,
    'page': 'Misc.',
    'category': 'All',
    'optional': False,
    'class': PageAll,
}

# page for Python files (PY)
PAGE_PY = {
    'version': 24200,
    'expire': 25100,
    'page': 'Programming',
    'category': 'Python',
    'optional': True,
    'class': PagePython,
}
