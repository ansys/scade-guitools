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

"""Provides extensions for new or existing controls."""

from enum import Enum
import os
from pathlib import Path
import re
from typing import (
    Any,
    Dict,  # noqa: F401  #used in a typing annotation
    List,
    Optional,
    Tuple,
)

from scade.tool.suite.gui.dialogs import browse_directory, file_open, file_save
from scade.tool.suite.gui.widgets import (
    Button,
    CheckBox,
    ComboBox as _ComboBox,
    EditBox,
    GroupBox,
    Label,
    ObjectComboBox as _ObjectComboBox,
    RadioButton,
    Widget,
)

import ansys.scade.guitools.csts as c


class PushButton(Button):
    """
    Defines a button control with a default size.

    Parameters
    ----------
    owner : Any
        Owner of the button.

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
        """Initialize the push button with the given parameters."""
        super().__init__(owner, name, x, y, w, h, **kwargs)


class Edit(EditBox):
    """
    Defines a edit box control with a default height.

    Parameters
    ----------
    owner : Any
        Owner of the edit control.

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
        """Initialize the edit control with the given parameters."""
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
        Owner of the control.

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
        """Initialize the static edit control with the given parameters."""
        self.label = Label(owner, text, x, y + 4, wl, h - 4)
        super().__init__(owner, x + wl, y, w - wl, h, **kwargs)
        self.owner = owner

    def set_visible(self, show: bool):
        """Show or hide the control."""
        super().set_visible(show)
        self.label.set_visible(show)


class FSM(Enum):
    """Mode for the file selector."""

    OPEN, SAVE, DIR = range(3)


class FileSelector(StaticEdit):
    """
    Defines a bundle made of a static, an edit, and a button control.

    Parameters
    ----------
    owner : Any
        Owner of the control.

    text : str
        Text of the static control.

    extension : str
        Default extension of the files.
        This option is ignored when ``mode`` is ``FSM.DIR``.

    directory : str
        Initial directory of the file selector dialog box, or the current directory when empty.

    filter : str
        Description of the format of the visible files in the file selector dialog box.
        This option is ignored when ``mode`` is ``FSM.DIR``.

    mode : FSM
        Mode of the file seclector dialog box, either ``FSM.LOAD``, ``FSM.SAVE``,
        or ``FSM.DIR`` for browsing directories.

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
        """Initialize the file selector with the given parameters."""
        super().__init__(owner, text, wl, x, y, w - c.DOTS_WIDTH - self._SEPARATOR, h, **kwargs)
        x_dots = x + w - c.DOTS_WIDTH
        # so that borders are aligned
        y_dots = y - 1
        self.btn_dots = Button(
            owner,
            '...',
            x_dots,
            y_dots,
            c.DOTS_WIDTH,
            c.DOTS_HEIGHT,
            on_click=self.on_click,
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
            """Expand environment variables in the given string."""
            # rename $(...) by ${...}
            name = re.sub(r'\$\(([^\)/\\\$]*)\)', r'${\1}', name)
            # resolve the environment variables, if any
            return os.path.expandvars(name)

        # wrong signature for Edit.get_name()
        name: str = self.get_name()  # type: ignore

        name = expand_vars(name)
        directory = expand_vars(self.directory)
        reference = expand_vars(self.reference)
        if not directory and reference:
            directory = reference
        # ensure Windows' path syntax
        directory = str(Path(directory))
        if self.mode == FSM.SAVE:
            path = file_save(name, self.extension, directory, self.filter)
        elif self.mode == FSM.OPEN:
            path = file_open(self.filter, directory)
        else:
            # assert self.mode == FSM.DIR
            path = browse_directory(directory)
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
    Defines a check box control with a default height.

    Parameters
    ----------
    owner : Any
        Owner of check button.

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
        self,
        owner,
        text: str,
        x: int,
        y: int,
        w: int,
        h: int = c.CHECK_BUTTON_HEIGHT,
        **kwargs,
    ):
        """Initialize the check button with the given parameters."""
        super().__init__(owner, text, x, y, w, h, **kwargs)
        self.owner = owner


class ComboBox(_ComboBox):
    """
    Defines a combo box control with a default height.

    Parameters
    ----------
    owner : Any
        Owner of the combo box control.

    x : int
        Horizontal position of the combo box control.

    y : int
        Vertical position of the combo box control.

    w : int
        Width of the combo box control.

    h : int
        Height of the combo box control, default csts.COMBO_BOX_HEIGHT.

    kwargs : Any
        Other parameters of ``scade.tool.suite.gui.widgets.ComboBox``.
    """

    def __init__(self, owner, x: int, y: int, w: int, h: int = c.COMBO_BOX_HEIGHT, **kwargs):
        """Initialize the combo box with the given parameters."""
        super().__init__(owner, [], x, y, w, h, **kwargs)
        self.owner = owner

    def on_layout(self):
        """Declare the constraints with respect to the owner."""
        self.set_constraint(Widget.RIGHT, self.owner, Widget.RIGHT, -c.RIGHT_MARGIN)


class ObjectComboBox(_ObjectComboBox):
    """
    Defines an object combo box control with a default height and extensions for serialization.

    This class provides an optional map to access an item with a string. This allows
    to persist the current selection in a file, or restore it from a value.

    Parameters
    ----------
    owner : Any
        Owner of the combo box control.

    x : int
        Horizontal position of the combo box control.

    y : int
        Vertical position of the combo box control.

    w : int
        Width of the combo box control.

    h : int
        Height of the combo box control, default csts.COMBO_BOX_HEIGHT.

    kwargs : Any
        Other parameters of ``scade.tool.suite.gui.widgets.ComboBox``.
    """

    def __init__(self, owner, x: int, y: int, w: int, h: int = c.COMBO_BOX_HEIGHT, **kwargs):
        """Initialize the object combo box with the given parameters."""
        super().__init__(owner, [], x, y, w, h, **kwargs)
        self.owner = owner
        self.items = []  # type: List[Any]
        self.names = []  # type: List[str]

    def on_layout(self):
        """Declare the constraints with respect to the owner."""
        self.set_constraint(Widget.RIGHT, self.owner, Widget.RIGHT, -c.RIGHT_MARGIN)

    def set_items(self, items: List[Any], names: Optional[List[str]] = None):
        """
        Set the combo box items, with an optional mapping.

        This mapping is used to serialize the selected item.
        """
        super().set_items(items)
        self.items = items
        self.names = names if names else []

    def get_selected_name(self) -> str:
        """Return the name of the selected item."""
        item = self.get_selection()
        try:
            name = self.names[self.items.index(item)]
        except ValueError:
            name = ''
        return name

    def select_name(self, name: str):
        """Select the item corresponding to name."""
        try:
            item = self.items[self.names.index(name)]
        except ValueError:
            item = None
        self.set_selection(item)


class StaticComboBox(ComboBox):
    """
    Defines a bundle made of a static and a combo box control.

    Parameters
    ----------
    owner : Any
        Owner of the control.

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
        Height of the control, default csts.COMBO_BOX_HEIGHT.

    kwargs : Any
        Other parameters of ``scade.tool.suite.gui.widgets.ComboBox``.
    """

    def __init__(
        self,
        owner,
        text: str,
        wl: int,
        x: int,
        y: int,
        w: int,
        h: int = c.COMBO_BOX_HEIGHT,
        **kwargs,
    ):
        """Initialize the static combo box with the given parameters."""
        self.label = Label(owner, text, x, y + 4, wl, c.STATIC_HEIGHT)
        super().__init__(owner, x + wl, y, w - wl, h, **kwargs)
        self.owner = owner

    def set_visible(self, show: bool):
        """Show or hide the control."""
        super().set_visible(show)
        self.label.set_visible(show)


class StaticObjectComboBox(ObjectComboBox):
    """
    Defines a bundle made of a static and an object combo box control.

    Parameters
    ----------
    owner : Any
        Owner of the control.

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
        Height of the control, default csts.COMBO_BOX_HEIGHT.

    kwargs : Any
        Other parameters of ``scade.tool.suite.gui.widgets.ObjectComboBox``.
    """

    def __init__(
        self,
        owner,
        text: str,
        wl: int,
        x: int,
        y: int,
        w: int,
        h: int = c.COMBO_BOX_HEIGHT,
        style: Optional[List[str]] = None,
        **kwargs,
    ):
        """Initialize the static object combo box with the given parameters."""
        if not style:
            style = []
        if 'dropdownlist' not in style:
            style.append('dropdownlist')
        self.label = Label(owner, text, x, y + 4, wl, c.STATIC_HEIGHT)
        super().__init__(owner, x + wl, y, w - wl, h, style=style, **kwargs)
        self.owner = owner

    def set_visible(self, show: bool):
        """Show or hide the control."""
        super().set_visible(show)
        self.label.set_visible(show)


class RadioBox(GroupBox):
    """
    Defines a bundle made of a group and a set of radio button controls.

    The group is hidden when text is empty.

    Parameters
    ----------
    owner : Any
        Owner of the control.

    buttons : list[tuple[str, str]]
        Descriptions of the buttons: value and text associated to the buttons.

    x : int
        Horizontal position of the control.

    y : int
        Vertical position of the control.

    w : int
        Width of the control.

    h : int
        Height of the control, default 0.

    text : str
        Text of the group control, default empty.

    kwargs : Any
        Other parameters of ``scade.tool.suite.gui.widgets.GroupBox``.
    """

    def __init__(
        self,
        owner,
        buttons: List[Tuple[str, str]],
        x: int,
        y: int,
        w: int,
        text: str = '',
        h: int = c.GROUP_RADIO_BOX_HEIGHT,
    ):
        """Initialize the radio box with the given parameters."""
        if text:
            # group visible
            offset_x = c.LEFT_MARGIN
            offset_y = c.STATIC_HEIGHT
            # width for buttons
            width = w - c.LEFT_MARGIN - c.RIGHT_MARGIN
        else:
            # group not visible
            offset_x = 0
            offset_y = 0
            width = w
            h = 0

        n = len(buttons)
        wb = int(width / n) if n > 0 else width
        self.buttons = {}  # type: Dict[str, RadioButton]
        self.owner = owner
        self.text = text
        # the group is used to set relative constraints
        super().__init__(owner, text, x, y, w, h)
        x = x + offset_x
        y = y + offset_y
        for value, text in buttons:
            button = RadioButton(owner, text, x, y, wb, c.RADIO_BUTTON_HEIGHT)
            self.buttons[value] = button
            x += wb
        Widget.group(self.buttons.values())

    def on_layout(self):
        """Declare the constraints with respect to the owner."""
        self.set_constraint(Widget.RIGHT, self.owner, Widget.RIGHT, -c.RIGHT_MARGIN)
        prev = None
        count = len(self.buttons)
        margin = c.LEFT_MARGIN + c.RIGHT_MARGIN if self.text else 0
        for button in self.buttons.values():
            if prev:
                button.set_constraint(Widget.LEFT, prev, Widget.RIGHT, 0)
            button.set_constraint(
                # wrong signature for set_constraint(), mul parameter must be float
                Widget.WIDTH,
                self,
                Widget.WIDTH,
                -int(margin / count),
                1.0 / count,  # type: ignore
            )
            # button.set_constraint(Widget.WIDTH, self, Widget.WIDTH, 0, 1. / count)
            prev = button

    def set_visible(self, show: bool):
        """Show or hide the control."""
        self.set_visible(show)
        for button in self.buttons.values():
            button.set_visible(show)

    def get_value(self) -> str:
        """Return the value of the selected button, or ``""`` when none is selected."""
        for value, button in self.buttons.items():
            if button.get_check():
                return value
        else:
            return ''

    def set_value(self, value: str):
        """
        Select the button corresponding to the input value.

        * No button is selected when ``value`` is ``""``.
        * The first button is selected if ``value`` does not correspond to any button.

        Parameters
        ----------
        value : str
            Input value corresponding to a button.
        """
        if value == '':
            # uncheck all buttons
            for button in self.buttons.values():
                button.set_check(False)
        else:
            if value not in self.buttons:
                value = list(self.buttons.keys())[0]
            for v, button in self.buttons.items():
                button.set_check(v == value)


class GroupRadioBox(RadioBox):
    """
    Defines a bundle made of a group and a set of radio button controls.

    Parameters
    ----------
    owner : Any
        Owner of the control.

    text : str
        Text of the group control.

    buttons : list[tuple[str, str]]
        Descriptions of the buttons: value and text associated to the buttons.

    x : int
        Horizontal position of the control.

    y : int
        Vertical position of the control.

    w : int
        Width of the control.

    h : int
        Height of the control, default csts.RADIO_BOX_HEIGHT.

    kwargs : Any
        Other parameters of ``scade.tool.suite.gui.widgets.GroupBox``.
    """

    def __init__(
        self,
        owner,
        text: str,
        buttons: List[Tuple[str, str]],
        x: int,
        y: int,
        w: int,
        h: int = c.GROUP_RADIO_BOX_HEIGHT,
    ):
        """Initialize the group radio box with the given parameters."""
        super().__init__(owner, buttons, x, y, w, text=text, h=h)


class StaticRadioBox(RadioBox):
    """
    Defines a bundle made of a static and a group of radio button controls.

    The group is not visible and is used to set relative constraints.

    Parameters
    ----------
    owner : Any
        Owner of the control.

    text : str
        Text of the static control.

    wl : int
        Width of the static control.

    buttons : list[tuple[str, str]]
        Descriptions of the buttons: value and text associated to the buttons.

    x : int
        Horizontal position of the control.

    y : int
        Vertical position of the control.

    w : int
        Width of the control.

    kwargs : Any
        Other parameters of ``scade.tool.suite.gui.widgets.GroupBox``.
    """

    def __init__(
        self,
        owner,
        text: str,
        wl: int,
        buttons: List[Tuple[str, str]],
        x: int,
        y: int,
        w: int,
    ):
        """Initialize the static radio box with the given parameters."""
        self.label = Label(owner, text, x=x, y=y + 4, w=wl, h=c.STATIC_HEIGHT)
        super().__init__(owner, buttons, x + wl, y, w - wl)

    def set_visible(self, show: bool):
        """Show or hide the control."""
        self.label.set_visible(show)
        super().set_visible(show)
