# -*- coding: utf-8 -*-

# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
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
from scade.tool.suite.gui.widgets import Button

import ansys.scade.guitools.csts as constants
from ansys.scade.guitools.dialog import DS, DialogBox


class EmptyDialogBox(DialogBox):
    """
    Empty dialog with callbacks for each button.

    The callbacks verify their connection by testing the name
    of the attached button control without the accelerator marker.
    """

    def __init__(self, style: DS):
        super().__init__('Buttons', 300, 150, style=style)

    def on_build_ex(self):
        # empty
        pass

    def on_click_close(self, *args):
        assert args[0].get_name().replace('&', '') == 'Close'
        super().on_click_close(*args)

    def on_click_yes(self, *args):
        assert args[0].get_name().replace('&', '') == 'Yes'
        super().on_click_yes(*args)

    def on_click_no(self, *args):
        assert args[0].get_name().replace('&', '') == 'No'
        super().on_click_no(*args)

    def on_click_ok(self, *args):
        assert args[0].get_name().replace('&', '') == 'OK'
        super().on_click_ok(*args)

    def on_click_cancel(self, *args):
        assert args[0].get_name().replace('&', '') == 'Cancel'
        super().on_click_cancel(*args)

    def on_click_retry(self, *args):
        assert args[0].get_name().replace('&', '') == 'Retry'
        super().on_click_retry(*args)


class _TestDialogBox(DialogBox):
    """Defines a sample dialog box to test the styles."""

    __test__ = False

    def __init__(self):
        super().__init__('TestDialogBox', 300, 250)

    def on_build_ex(self):
        """Build the dialog."""
        # add a button per style
        x = constants.LEFT_MARGIN
        y = constants.TOP_MARGIN
        w = 200
        h = constants.BUTTON_HEIGHT
        for style in DS:
            Button(self, style.name, x, y, w, h, self.on_click_button)
            y += constants.BUTTON_HEIGHT + constants.TOP_MARGIN

        # add a Close button at the bottom-right position
        w = constants.BUTTON_WIDTH
        h = constants.BUTTON_HEIGHT
        x = self.right - w
        y = self.bottom - h
        Button(self, '&Close', x, y, w, h, self.on_click_close)

    def on_click_button(self, button):
        style = DS[button.get_name()]
        EmptyDialogBox(style).do_modal()

    def on_click_close(self, *args):
        """Close the dialog."""
        self.close()


class CommandTestDialogBox(Command):
    """Defines a command to display a dialog box."""

    def __init__(self):
        label = 'DialogBox'
        super().__init__(name=f'&{label}...', status_message=label, tooltip_message=label)

    def on_activate(self):
        """Open the dialog."""
        _TestDialogBox().do_modal()
