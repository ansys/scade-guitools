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

from enum import Enum
import os
from pathlib import Path
import re
from typing import Any

from scade.tool.suite.gui.dialogs import file_open, file_save
from scade.tool.suite.gui.widgets import (
    Button,
    CheckBox,
    EditBox,
    Label,
    Widget,
)

import ansys.scade.guitools.csts as c


class PushButton(Button):
    """
    Defines a push button control with a default size.

    Parameters
    ----------
    owner : Any
        owner of the button

    name : str
        Name of the button.

    x : int
        Horizontal position of the push button.

    y : int
        Vertical position of the push button.

    w : int
        Width of the push button, default csts.BUTTON_WIDTH.

    h : int
        Height of the push button, default csts.BUTTON_HEIGHT.

    kwargs : Any
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


class Edit(EditBox):
    """
    Defines a edit control with a default height.

    Parameters
    ----------
    owner : Any
        owner of edit control

    x : int
        Horizontal position of the edit control.

    y : int
        Vertical position of the edit control.

    w : int
        Width of the edit control.

    h : int
        Height of the edit control, default csts.EDIT_HEIGHT.

    kwargs : Any
        Other parameters of ``scade.tool.suite.gui.widgets.EditBox``.
    """

    def __init__(self, owner, x: int, y: int, w: int, h: int = c.EDIT_HEIGHT, **kwargs):
        super().__init__(owner, x, y, w, h, **kwargs)
        self.owner = owner

    def on_layout(self):
        """Declare the constraints with respect to the owner."""
        self.set_constraint(Widget.RIGHT, self.owner, Widget.RIGHT, -c.RIGHT_MARGIN)


class StaticEdit(Edit):
    """
    Defines a bundle made of a static and an edit control.

    Parameters
    ----------
    owner : Any
        owner of the control

    text : str
        Text of the static control.

    wl : int
        Width of the static control.

    x : int
        Horizontal position of the control.

    y : int
        Vertical position of the control.

    w : int
        Width of the control.

    h : int
        Height of the control, default csts.EDIT_HEIGHT.

    kwargs : Any
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

    def set_visible(self, show: bool):
        """Show or hide the control."""
        super().set_visible(show)
        self.label.set_visible(show)


class FSM(Enum):
    """Mode for the file selector."""

    OPEN, SAVE = range(2)


class FileSelector(StaticEdit):
    """
    Defines a bundle made of a static, an edit, and a button control.

    Parameters
    ----------
    owner : Any
        owner of the control

    text : str
        Text of the static control.

    extension : str
        Default extension of the files.

    directory : str
        Initial directory of the file selector dialog box, or the current directory when empty.

    filter : str
        Description of the format of the visible files in the file selector dialog box.

    mode : FSM
        Mode of the file seclector dialog box, either ``FSM.LOAD`` or ``FSM.SAVE``.

    wl : int
        Width of the static control.

    x : int
        Horizontal position of the control.

    y : int
        Vertical position of the control.

    w : int
        Width of the control.

    h : int
        Height of the control, default csts.EDIT_HEIGHT.

    reference : str
        Reference directory to resolve or compute a relative path when not empty.

    kwargs : Any
        Other parameters of ``scade.tool.suite.gui.widgets.EditBox``.
    """

    # separator between the edit and the button controls
    _SEPARATOR = 5

    def __init__(
        self,
        owner,
        text: str,
        extension: str,
        directory: str,
        filter: str,
        mode: FSM,
        wl: int,
        x: int,
        y: int,
        w: int,
        h: int = c.EDIT_HEIGHT,
        reference: str = '',
        **kwargs,
    ):
        super().__init__(owner, text, wl, x, y, w - c.DOTS_WIDTH - self._SEPARATOR, h, **kwargs)
        x_dots = x + w - c.DOTS_WIDTH
        # so that borders are aligned
        y_dots = y - 1
        self.btn_dots = Button(
            owner, '...', x_dots, y_dots, c.DOTS_WIDTH, c.DOTS_HEIGHT, on_click=self.on_click
        )
        self.owner = owner
        self.extension = extension
        self.directory = directory
        self.filter = filter
        self.mode = mode
        self.reference = reference

    def on_click(self, button: Button):
        """Call the Windows standard open or save selection commands."""

        def expand_vars(name: str) -> str:
            # rename $(...) by ${...}
            name = re.sub(r'\$\(([^\)/\\\$]*)\)', r'${\1}', name)
            # resolve the environment variables, if any
            return os.path.expandvars(name)

        name = self.get_name()  # type: str  # wrong signature for get_name()

        name = expand_vars(name)
        directory = expand_vars(self.directory)
        reference = expand_vars(self.reference)
        if not directory and reference:
            directory = reference
        # ensure Windows' path syntax
        directory = str(Path(directory))
        if self.mode == FSM.SAVE:
            path = file_save(name, self.extension, directory, self.filter)
        else:
            path = file_open(self.filter, directory)
        if path:
            if reference:
                try:
                    path = os.path.relpath(path, reference)
                except ValueError:
                    pass
            self.set_name(path)

    def on_layout(self):
        """Declare the constraints with respect to the owner."""
        self.btn_dots.set_constraint(Widget.RIGHT, self.owner, Widget.RIGHT, -c.RIGHT_MARGIN)
        self.btn_dots.set_constraint(
            Widget.LEFT, self.owner, Widget.RIGHT, -c.RIGHT_MARGIN - c.DOTS_WIDTH
        )
        self.set_constraint(Widget.RIGHT, self.btn_dots, Widget.LEFT, -self._SEPARATOR)

    def set_visible(self, show: bool):
        """Show or hide the control."""
        super().set_visible(show)
        self.btn_dots.set_visible(show)


class CheckButton(CheckBox):
    """
    Defines a check button control with a default height.

    Parameters
    ----------
    owner : Any
        owner of check button

    text : str
        Text of check button.

    x : int
        Horizontal position of the check button.

    y : int
        Vertical position of the check button.

    w : int
        Width of the check button.

    h : int
        Height of the check button, default csts.CHECK_BUTTON_HEIGHT.

    kwargs : Any
        Other parameters of ``scade.tool.suite.gui.widgets.CheckBox``.
    """

    def __init__(
        self, owner, text: str, x: int, y: int, w: int, h: int = c.CHECK_BUTTON_HEIGHT, **kwargs
    ):
        super().__init__(owner, text, x, y, w, h, **kwargs)
        self.owner = owner
