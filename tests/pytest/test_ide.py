# -*- coding: utf-8 -*-

# Copyright (C) 2024 - 2026 ANSYS, Inc. and/or its affiliates.
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


"""Unit tests for IDE abstraction."""

from pathlib import Path

from ide.run import run

from ansys.scade.guitools.stubs import StubIde
from conftest import diff_files, load_session


def test_ide_nominal():
    path_model = Path(__file__).parent / 'ide' / 'Model.etp'
    ide = StubIde()

    ide.session = load_session(path_model, with_project=True)
    ide.project = ide.session.model.project
    run(ide)

    # additional tests
    cwd = path_model.parent
    log_browser = cwd / 'BROWSER.json'
    ide.save_browser(log_browser)
    ref_browser = log_browser.with_suffix('.ref')
    failed = diff_files(ref_browser, log_browser)
    assert not failed
