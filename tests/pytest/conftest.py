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


import difflib
import os
from pathlib import Path

# shall modify sys.path to access SCADE APIs
import ansys.scade.apitools  # noqa: F401

# isort: split

import scade
import scade.model.project.stdproject as std
import scade.model.suite as suite


def load_session(path: Path, with_project: bool = False) -> suite.Session:
    """
    Create an instance of Session and load the requested models.
    """
    session = suite.Session()
    session.load2(str(path))
    if with_project:
        session.model.project = load_project(path)
    return session


def load_project(path: Path) -> std.Project:
    """
    Load a Scade project in a separate environment.

    Note: uses ``scade.load_project`` undocumented API.
    """
    project = scade.load_project(str(path))  # type: ignore  # load_project is added dynamically
    return project


def cmp_file(reference: Path, result: Path, n=3, linejunk=None):
    """Return the differences between the reference and the result file."""
    # reference: replace $(ROOT) and $(DIR)with runtime data
    ref_lines = reference.open().read().split('\n')
    root = str(Path(__file__).parent.parent.parent).replace('\\', '\\\\')
    ref_lines = [
        _.replace('$(ROOT)', root).replace('$(DIR)', str(result.parent).replace('\\', '\\\\'))
        for _ in ref_lines
    ]
    with result.open() as f:
        if linejunk:
            res_lines = [_ for _ in f if not linejunk(_)]
        else:
            res_lines = f.read().split('\n')

    diff = difflib.context_diff(ref_lines, res_lines, str(reference), str(result), n=n)
    return diff


def diff_files(ref: Path, dst: Path) -> bool:
    print('compare', str(ref), str(dst))
    diffs = cmp_file(ref, dst)
    failure = False
    for d in diffs:
        print(d.rstrip('\r\n'))
        failure = True
    return failure


def diff_directories(ref_dir: Path, dst_dir: Path) -> bool:
    failure = False
    for reference in (ref_dir).glob('**/*'):
        if reference.is_dir():
            continue
        base = os.path.relpath(reference, ref_dir)
        target = dst_dir / base
        print('compare', str(reference), str(target))
        try:
            diff = cmp_file(reference, target, n=0)
        except BaseException as e:
            diff = [str(e)]
        # not captured, thus the loop hereafter
        # stdout.writelines(diff)
        local_failure = False
        for line in diff:
            print(line, end='')
            local_failure = True
        if local_failure:
            failure = True
            print()
    return failure
