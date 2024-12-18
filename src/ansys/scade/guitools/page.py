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

"""Extension for the Page classes."""

from typing import Any, Callable

from scade.model.project.stdproject import Configuration, Project
from scade.tool.suite.gui.properties import Page as PropertyPage
from scade.tool.suite.gui.settings import Page as SettingsPage

from ansys.scade.guitools.control import (
    FSM,
    CheckButton,
    ComboBox,
    Edit,
    FileSelector,
    ObjectComboBox,
    StaticComboBox,
    StaticEdit,
    StaticObjectComboBox,
)
import ansys.scade.guitools.csts as c

# width of fields, second column: unused since the controls are sized automatically
_WF = 100


class ContainerPage:
    """
    Base class for property or settings pages.

    It maintains a list of controls for automatic layout,
    or to show or hide an entire page.

    The controls are automatically added on two columns: labels and edits.

    Parameters
    ----------
    label_width : int
        Width of the first column.
    """

    def __init__(self, label_width: int):
        self.label_width = label_width
        self.controls = []

    def add_edit(self, y: int, **kwargs) -> Edit:
        """Add a :class:`Edit <ansys.scade.guitools.control.Edit>` control to the page."""
        edit = Edit(self, c.LEFT_MARGIN, y, _WF, **kwargs)
        self.controls.append(edit)
        return edit

    def add_static_edit(self, y: int, text: str, **kwargs) -> StaticEdit:
        """Add a :class:`StaticEdit <ansys.scade.guitools.control.StaticEdit>` control to the page."""
        edit = StaticEdit(self, text, self.label_width, c.LEFT_MARGIN, y, _WF, **kwargs)
        self.controls.append(edit)
        return edit

    def add_file_selector(
        self, y: int, text: str, extension: str, dir: str, filter: str, mode: FSM, **kwargs
    ) -> FileSelector:
        """Add a :class:`FileSelector <ansys.scade.guitools.control.FileSelector>` to the page."""
        file = FileSelector(
            self,
            text,
            extension,
            dir,
            filter,
            mode,
            self.label_width,
            c.LEFT_MARGIN,
            y,
            _WF,
            **kwargs,
        )
        self.controls.append(file)
        return file

    def add_check_button(self, y: int, text: str, **kwargs) -> CheckButton:
        """Add a :class:`CheckButton <ansys.scade.guitools.control.CheckButton>` control to the page."""
        cb = CheckButton(self, text, c.LEFT_MARGIN, y, _WF, **kwargs)
        self.controls.append(cb)
        return cb

    def add_combo_box(self, y: int, text: str, **kwargs) -> ComboBox:
        """Add a :class:`ComboBox <ansys.scade.guitools.control.ComboBox>` control to the page."""
        cb = ComboBox(self, c.LEFT_MARGIN, y, _WF, **kwargs)
        self.controls.append(cb)
        return cb

    def add_object_combo_box(self, y: int, text: str, **kwargs) -> ObjectComboBox:
        """Add a :class:`ObjectComboBox <ansys.scade.guitools.control.ObjectComboBox>` control to the page."""
        cb = ObjectComboBox(self, c.LEFT_MARGIN, y, _WF, **kwargs)
        self.controls.append(cb)
        return cb

    def add_static_combo_box(self, y: int, text: str, **kwargs) -> StaticComboBox:
        """Add a :class:`StaticComboBox <ansys.scade.guitools.control.StaticComboBox>` control to the page."""
        cb = StaticComboBox(self, text, self.label_width, c.LEFT_MARGIN, y, _WF, **kwargs)
        self.controls.append(cb)
        return cb

    def add_static_object_combo_box(self, y: int, text: str, **kwargs) -> StaticObjectComboBox:
        """Add a :class:`StaticObjectComboBox <ansys.scade.guitools.control.StaticObjectComboBox>` control to the page."""
        cb = StaticObjectComboBox(self, text, self.label_width, c.LEFT_MARGIN, y, _WF, **kwargs)
        self.controls.append(cb)
        return cb

    def add_control(self, control):
        """Add an existing control to the page's list of controls."""
        self.controls.append(control)

    def layout_controls(self):
        """Declare the contained control's constraints."""
        for control in self.controls:
            try:
                control.on_layout()
            except AttributeError:
                # ignore exception for controls not defining the function
                pass

    def show_controls(self, show: bool):
        """Show or hide the contained controls."""
        for control in self.controls:
            control.set_visible(show)


class SettingsPageEx(SettingsPage, ContainerPage):
    """
    Provides a base class for settings pages.

    This class also provides means to manage the persistence
    of most common controls in the project.

    .. Note::

        Do not forget to call ``super().on_build()`` in your ``on_build``
        redefinition. Otherwise, you may experience crashes the next time
        the settings dialog is open.
    """

    def __init__(self, label_width: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super(SettingsPage, self).__init__(label_width)
        # get, set, tool, prop, prop_default
        self.properties = []  # type: List[Tuple[Callable, Callable, str, str, str]]

    def on_build(self):
        """
        Reset the lists used for persistence or resizing.

        This method **must** be called by the derived classes' ``on_build`` methods.
        """
        self.controls = []
        self.properties = []

    def on_layout(self):
        """Specify how controls are moved or resized."""
        self.layout_controls()

    def declare_property(
        self, pfnget: Callable, pfnset: Callable, tool: str, name: str, default: Any
    ):
        """
        Declare a scalar property for automatic management.

        When the page is displayed, it is updated with the declared properties
        that are read from the project.
        When the page is validated, the project is updated with the declared
        properties that are read from its controls.

        The values are persisted in the project as *Tool Properties*, that are
        properties named as ``@<TOOL>:<NAME>``, associated to a configuration.

        Example
        -------

        .. code-block::

            edit = self.add_edit(y)
            self.declare_property(edit.get_name, edit.set_name, 'MY_TOOL', 'MY_PROP', '')
            y += 30
            cb = self.add_check_button(y, 'Option')
            self.declare_property(cb.get_check, cb.set_check, 'MY_TOOL', 'MY_OPTION', False)
            y += 30

        Parameters
        ----------
        pfnget : Callable
            Function to retrieve a value from a control such as ``Edit.get_name()``
            or ``CheckBox.get_check()``.

        pfnset : Callable
            Function to set a value to a control such as ``Edit.set_name()``
            or ``CheckBox.set_check()``.

        tool : str
            Name of the tool.

        name :
            Name of the property.

        default : Any
            Default value of the property.
        """
        self.properties.append((pfnget, pfnset, tool, name, default))

    def on_display(self, project: Project, configuration: Configuration):
        """Update the page with the properties read from the project."""
        for _, pfnset, tool, name, default in self.properties:
            if isinstance(default, bool):
                value = project.get_bool_tool_prop_def(tool, name, default, configuration)
            else:
                value = project.get_scalar_tool_prop_def(tool, name, default, configuration)
            pfnset(value)

    def on_validate(self, project: Project, configuration: Configuration):
        """Update the project with the properties read from the page."""
        for pfnget, _, tool, name, default in self.properties:
            value = pfnget()
            if isinstance(value, bool):
                project.set_bool_tool_prop_def(tool, name, value, default, configuration)
            else:
                project.set_scalar_tool_prop_def(tool, name, value, default, configuration)


class PropertyPageEx(PropertyPage, ContainerPage):
    """
    Provides a base class for property pages.

    This class also provides means to manage the sizing
    of most common controls.

    .. Note::

        Do not forget to call ``super().on_build()`` in your ``on_build``
        redefinition. Otherwise, you may experience random crashes.
    """

    def __init__(self, label_width: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super(PropertyPage, self).__init__(label_width)

    def on_build(self):
        """
        Reset the lists used for resizing.

        This method **must** be called by the derived classes' ``on_build`` methods.
        """
        self.controls = []

    def on_layout(self):
        """Specify how controls are moved or resized."""
        self.layout_controls()
