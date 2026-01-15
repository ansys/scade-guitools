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

"""
Provides a SCADE IDE Command base class.

This module provides Command base class that stubs
``scade.tool.suite.gui.commands.Command`` when not available.

This allows to create unit tests for commands.
"""

from ansys.scade.guitools.ide import Ide

try:
    from scade.tool.suite.gui.commands import Command as _Command  # type: ignore
except ImportError:
    import scade

    scade.output('IDE stub activated\n')  # type: ignore

    class _Command:
        """Stub for ``scade.tool.suite.gui.commands.Command``."""

        def __init__(
            self,
            name: str,
            status_message: str,
            tooltip_message: str,
            image_file: str = '',
        ):
            self.name = name
            self.status_message = status_message
            self.tooltip_message = tooltip_message
            self.image_file = image_file

        def on_enable(self) -> bool:
            """Return whether the command can be activated, ``True`` by default."""
            return True

        def on_activate(self):
            """Run the command."""
            pass


class Command(_Command):
    """
    Base class for commands.

    Parameters
    ----------
    ide : Ide
        SCADE IDE abstraction.
    """

    def __init__(self, ide: Ide, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ide = ide
