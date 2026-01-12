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

"""Test extension Ansys SCADE GUI Tools."""

import traceback

import scade
from scade.tool.suite.gui.commands import Command, Menu

from ansys.scade.guitools import __version__
from ansys.scade.guitools.enable_debugpy import attach_to_debugger

# isort: split
# test modules
from test_control import CommandTestControl
from test_dialog_box import CommandTestDialogBox
from test_pragmas import TestPragmaPropertyPage
from test_properties import TestPropertyPage
from test_settings import TestSettingsPage

# display some banner
# scade is a CPython module defined dynamically
scade.tabput('LOG', f'Loading integration tests for Ansys SCADE GUI Tools {__version__}.\n')  # type: ignore


def main():
    Menu(
        [
            CommandTestDialogBox(),
            CommandTestControl(),
            Command.SEPARATOR,
            CommandAttachToDebugger(),
        ],
        '&Tools/Test GUI Tools',
    )
    TestSettingsPage()
    TestPropertyPage()
    TestPragmaPropertyPage()


class CommandAttachToDebugger(Command):
    """Defines a command to display a dialog box."""

    def __init__(self):
        label = 'Attach to Debugger'
        super().__init__(name=label, status_message=label, tooltip_message=label)

    def on_activate(self):
        """Open the dialog."""
        attach_to_debugger()


try:
    main()
except BaseException as e:
    scade.tabput('LOG', f'{e}\n')  # type: ignore
    scade.tabput('LOG', f'{traceback.format_exc()}\n')  # type: ignore
else:
    scade.tabput('LOG', f'Integration tests for Ansys SCADE GUI Tools {__version__} loaded.\n')  # type: ignore
