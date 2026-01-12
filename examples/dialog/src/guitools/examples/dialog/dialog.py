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

"""Example of dialog box."""

import scade
from scade.tool.suite.gui.commands import Command, Menu

from ansys.scade.guitools.control import StaticEdit
import ansys.scade.guitools.csts as c
from ansys.scade.guitools.dialog import DS, DialogBox


class ExampleDialogBox(DialogBox):
    """Defines a sample dialog box with 2 fields."""

    def __init__(self, f1: str, f2: str):
        super().__init__('Example GUI Tools DialogBox', 300, 150, style=DS.OK_CANCEL)
        # initial values
        self.f1 = f1
        self.f2 = f2

    def on_build_ex(self):
        """Build the dialog with 2 controls."""
        # initial position and sizes
        x = c.LEFT_MARGIN
        y = c.TOP_MARGIN
        # width of first column
        wl = 100
        # overall width: remove the margins
        w = self.right - c.LEFT_MARGIN - c.RIGHT_MARGIN
        self.ed_f1 = StaticEdit(self, 'f1', wl, x, y, w, name=self.f1)
        y += c.DY
        self.ed_f2 = StaticEdit(self, 'f2', wl, x, y, w, name=self.f2)

    def on_click_ok(self, *args):
        """Update the values and close the dialog."""
        self.f1 = self.ed_f1.get_name()
        self.f2 = self.ed_f2.get_name()
        super().on_click_ok()


class CommandExampleDialogBox(Command):
    """Defines a command to display a dialog box."""

    def __init__(self):
        label = 'GUI Tools DialogBox'
        super().__init__(name=f'&{label}...', status_message=label, tooltip_message=label)

    def on_activate(self):
        """Open the dialog box."""
        dlg = ExampleDialogBox('value1', 'value2')
        # open the dialog box
        dlg.do_modal()
        # display the values
        # scade is a CPython module defined dynamically
        scade.tabput('LOG', f'f1 = "{dlg.f1}", f2 = "{dlg.f2}"\n')  # type: ignore


Menu([Command.SEPARATOR, CommandExampleDialogBox(), Command.SEPARATOR], '&Help/Examples')
