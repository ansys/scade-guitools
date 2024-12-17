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

"""Provides extensions for existing controls or new ones."""

from typing import Any

from scade.tool.suite.gui.widgets import Button, EditBox, Label, Widget

import ansys.scade.guitools.csts as c


class PushButton(Button):
    """
    Defines a push button control with a default size.

    Parameters
    ----------
    owner: Any
        owner of the button

    name: str
        Name of the button.

    x: int
        Horizontal position of the push button.

    y: int
        Vertical position of the push button.

    w: int
        Width of the push button, default csts.BUTTON_WIDTH.

    h: int
        Height of the push button, default csts.BUTTON_HEIGHT.

    kwargs: Any
        Other parameters of ``scade.tool.suite.gui.widgets.Button``.
    """

    def __init__(
        self,
        owner: Any,
        name: str,
        x: int,
        y: int,
        w: int = c.BUTTON_WIDTH,
        h: int = c.BUTTON_HEIGHT,
        **kwargs,
    ):
        super().__init__(owner, name, x, y, w, h, **kwargs)


class StaticEdit(EditBox):
    """
    Defines a bundle made of a static and an edit control.

    Parameters
    ----------
    owner: Any
        owner of the control

    text: str
        Text of the static control.

    wl: int
        Width of the static control.

    x: int
        Horizontal position of the control.

    y: int
        Vertical position of the control.

    w: int
        Width of the control.

    h: int
        Height of the control, default csts.EDIT_HEIGHT.

    kwargs: Any
        Other parameters of ``scade.tool.suite.gui.widgets.EditBox``.
    """

    def __init__(
        self,
        owner,
        text: str,
        wl: int,
        x: int,
        y: int,
        w: int,
        h: int = c.EDIT_HEIGHT,
        **kwargs,
    ):
        self.label = Label(owner, text, x, y + 4, wl, h - 4)
        super().__init__(owner, x + wl, y, w - wl, h, **kwargs)
        self.owner = owner

    def on_layout(self):
        """Declare the constraints with respect to the owner."""
        self.set_constraint(Widget.RIGHT, self.owner, Widget.RIGHT, -c.RIGHT_MARGIN)

    def set_visible(self, show: bool):
        """Show or hide the control."""
        super().set_visible(show)
        self.label.set_visible(show)
