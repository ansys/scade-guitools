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

"""Provides an extension for the Dialog class."""

from abc import abstractmethod
from enum import Enum

from scade.tool.suite.gui.dialogs import Dialog
from scade.tool.suite.gui.widgets import Button

import ansys.scade.guitools.csts as c


class DS(Enum):
    """Style for dialog box validation buttons."""

    NONE, CLOSE, OK_CANCEL, RETRY_CANCEL, YES_NO, YES_NO_CANCEL = range(6)


class DialogBox(Dialog):
    """
    Defines a dialog box with optional default button management.

    Parameters
    ----------
    title: str
        Title of the dialog box.

    width: int
        Width of the client area if ``nc`` is ``False``, otherwise
        overall width of the dialog box.

    height: int
        Height of the client area if ``nc`` is ``False``, otherwise
        overall width of the dialog box.

    nc: bool
        Whether the provided dimensions are for the overall dialog box
        or for its client area, default ``False``.

    kwargs: Any
        Other parameters of ``scade.tool.suite.gui.dialog.Dialog``.
    """

    def __init__(
        self, title: str, width: int, height: int, nc: bool = False, style: DS = DS.NONE, **kwargs
    ):
        """Initialize the dialog box."""
        if not nc:
            # increase the bounding box with NC margins
            width += c.NC_RIGHT + c.NC_LEFT
            height += c.NC_TOP + c.NC_BOTTOM
        super().__init__(title, width, height, **kwargs)

        # store instantiation parameters
        self._nc = nc
        self._style = style
        # buttons, depending on style
        self._buttons = []

    @property
    def right(self) -> int:
        """
        Return the right-most position of the dialog box.

        This corresponds to the width of its client area.
        """
        return self.width - (c.NC_RIGHT + c.NC_LEFT)

    @property
    def bottom(self) -> int:
        """
        Return the bottom-most position of the dialog box.

        This corresponds to the height of its client area
        if there are no buttons, otherwise the vertical position
        of the bottom buttons.
        """
        bottom = self.height - (c.NC_TOP + c.NC_BOTTOM)
        if self._style != DS.NONE:
            bottom -= c.BUTTON_HEIGHT + c.BOTTOM_MARGIN
        return bottom

    def on_build(self):
        """Build the dialog with the specified dialog validation buttons."""
        # build the controls
        self.on_build_ex()
        # add the validation buttons
        descriptions = [
            ('Close', self.on_click_close, (DS.CLOSE,)),
            ('OK', self.on_click_ok, (DS.OK_CANCEL,)),
            ('Retry', self.on_click_retry, (DS.RETRY_CANCEL,)),
            ('&Yes', self.on_click_yes, (DS.YES_NO, DS.YES_NO_CANCEL)),
            ('&No', self.on_click_no, (DS.YES_NO, DS.YES_NO_CANCEL)),
            ('Cancel', self.on_click_cancel, (DS.OK_CANCEL, DS.RETRY_CANCEL, DS.YES_NO_CANCEL)),
        ]
        selection = [_ for _ in descriptions if self._style in _[-1]]
        self._buttons = []
        # separation between two buttons
        separator = c.RIGHT_MARGIN
        if selection:
            count = len(selection)
            # coordinates relative to the client area
            # dialog's dimensions include the non-client area
            x = self.right - count * (c.BUTTON_WIDTH + separator)
            y = self.bottom
            for label, callback, _ in selection:
                button = Button(self, label, x, y, c.BUTTON_WIDTH, c.BUTTON_HEIGHT, callback)
                self._buttons.append(button)
                x += c.BUTTON_WIDTH + separator

    def on_click_close(self, *args):
        """Close the dialog when Close is pressed."""
        self.close()

    def on_click_yes(self, *args):
        """Close the dialog when Yes is pressed."""
        self.close()

    def on_click_no(self, *args):
        """Close the dialog when No is pressed."""
        self.close()

    def on_click_ok(self, *args):
        """Close the dialog when OK is pressed."""
        self.close()

    def on_click_cancel(self, *args):
        """Close the dialog when Cancel is pressed."""
        self.close()

    def on_click_retry(self, *args):
        """Close the dialog when Retry is pressed."""
        self.close()

    @abstractmethod
    def on_build_ex(self):
        """Build the controls."""
        raise NotImplementedError
