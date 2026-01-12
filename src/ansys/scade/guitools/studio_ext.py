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

"""``Ide`` interface implementation for custom extensions."""

# this module uses `type: ignore` pragmas for ``scade`` functions: they
# are defined dynamically when the interpreter is created: typing analysis
# is not possible

from scade.tool.suite.gui import (
    dialogs,
    # functions defined dynamically
    register_load_model_callable,  # type: ignore
    register_terminate_callable,  # type: ignore
    register_unload_model_callable,  # type: ignore
)

from ansys.scade.guitools.studio import Studio


class StudioExt(Studio):
    """Implementation for SCADE IDE."""

    # Custom Dialogs

    def message_box(
        self, name: str, message: str, style: str = 'ok', icon: str = 'information'
    ) -> int:
        """Redirect the call to the API."""
        return dialogs.message_box(name, message, style, icon)

    def file_open(self, filter: str = '', directory: str = '') -> str:
        """Redirect the call to the API."""
        return dialogs.file_open(filter, directory)

    def file_save(
        self, file_name: str, extension: str = '', directory: str = '', filter: str = ''
    ) -> str:
        """Redirect the call to the API."""
        return dialogs.file_save(file_name, extension, directory, filter)

    def browse_directory(self, initial_directory: str = '') -> str:
        """Redirect the call to the API."""
        return dialogs.browse_directory(initial_directory)

    # Callback Registration

    def register_terminate_callable(self, callable):
        """Redirect the call to the API."""
        register_terminate_callable(callable)

    def register_load_model_callable(self, callable):
        """Redirect the call to the API."""
        register_load_model_callable(callable)

    def register_unload_model_callable(self, callable):
        """Redirect the call to the API."""
        register_unload_model_callable(callable)


studio = StudioExt()
