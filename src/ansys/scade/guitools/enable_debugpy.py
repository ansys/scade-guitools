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

"""
Enables remote debugging with ``debugpy``.

Refer to :ref:`Debug <contributing_debug>` for more information.
"""

import os
from pathlib import Path

import debugpy

os.environ['PYDEVD_LOAD_NATIVE_LIB'] = '0'
os.environ['PYDEVD_USE_CYTHON'] = '0'

# get the python interpreter, can't use sys.executable which is VCS.EXE
_os_module_path = Path(os.__file__).resolve().parent
_python_exe = _os_module_path / '..' / 'python.exe'

debugpy.configure(python=str(_python_exe))


def attach_to_debugger(port: int = 5678):
    """Start the debug server and wait for a client to connect."""
    debugpy.listen(port)
    debugpy.wait_for_client()
