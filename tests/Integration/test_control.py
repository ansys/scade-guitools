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

"""Test extension Ansys SCADE GUI Tools."""

from scade.tool.suite.gui.commands import Command

from ansys.scade.guitools.control import PushButton, StaticEdit
import ansys.scade.guitools.csts as c
from ansys.scade.guitools.dialog import DS, DialogBox


class _TestControl(DialogBox):
    """Defines a sample dialog box to test the controls."""

    __test__ = False

    def __init__(self):
        super().__init__('TestControl', 300, 250, style=DS.CLOSE)

    def on_build(self):
        """Build the dialog."""
        super().on_build()
        x = c.LEFT_MARGIN
        y = c.TOP_MARGIN
        dy = 30
        # add a push button
        PushButton(self, 'Button', x, y)
        y += dy
        # add a static + edit
        wl = 100
        w = self.right - c.LEFT_MARGIN - c.RIGHT_MARGIN
        StaticEdit(self, 'Static', wl, x, y, w, name='Edit')
        y += dy


class CommandTestControl(Command):
    """Defines a command to display a dialog box."""

    def __init__(self):
        label = 'Control'
        super().__init__(name=f'&{label}...', status_message=label, tooltip_message=label)

    def on_activate(self):
        """Open the dialog."""
        _TestControl().do_modal()
