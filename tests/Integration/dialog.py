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
from scade.tool.suite.gui.dialogs import Dialog
from scade.tool.suite.gui.widgets import Button

import ansys.scade.guitools.csts as c

_TITLE = 'Sample Dialog Box'
# usable dimensions
_WIDTH = 500
_HEIGHT = 300

H_BUTTON = 23
W_MARGIN = 15
H_MARGIN = 7


class _SampleDialog(Dialog):
    """Defines a sample dialog box."""

    def __init__(self):
        # increase the bounding box with NC margins
        super().__init__(_TITLE, _WIDTH + c.NC_RIGHT + c.NC_LEFT, _HEIGHT + c.NC_TOP + c.NC_BOTTOM)

        # controls
        self.btn_close = None

    def on_build(self):
        """Build the dialog."""
        # add a Close button at the bottom-right position
        w = 100
        h = H_BUTTON

        x = _WIDTH - w
        y = _HEIGHT - h

        Button(self, '&Close', x=x, y=y, w=w, h=h, on_click=self.on_click_close)

    def on_click_close(self, *args):
        """Close the dialog."""
        self.close()


class CommandSampleDialog(Command):
    """Defines a command to display a dialog box."""

    def __init__(self):
        super().__init__(name='Dialog...', status_message='Dialog', tooltip_message='Dialog')

    def on_activate(self):
        """Open the dialog."""
        _SampleDialog().do_modal()
