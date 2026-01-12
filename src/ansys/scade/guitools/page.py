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

"""Provides an extension for the Page classes."""

from abc import abstractmethod
from typing import Any, Callable, List, Optional, Tuple, Union

from scade.model.project.stdproject import Configuration, Project
from scade.tool.suite.gui.properties import Page as PropertyPage
from scade.tool.suite.gui.settings import Page as SettingsPage

from ansys.scade.guitools.control import (
    FSM,
    CheckButton,
    ComboBox,
    Edit,
    FileSelector,
    GroupRadioBox,
    ObjectComboBox,
    RadioBox,
    StaticComboBox,
    StaticEdit,
    StaticObjectComboBox,
    StaticRadioBox,
)
import ansys.scade.guitools.csts as c
from ansys.scade.guitools.interfaces import (
    IGuiHostClient,
    IPropertiesDataExchange,
    ISettingsDataExchange,
)

# width of fields, second column: unused since the controls are sized automatically
_WF = 100

Page = Union[PropertyPage, SettingsPage]

Getter = Callable[[], Any]
"""Signature for getting control's value."""
Setter = Callable[[Any], None]
"""Signature for setting control's value."""


class ContainerPage:
    """
    Base class for property or settings pages.

    It maintains a list of controls for automatic layout,
    or to show or hide an entire page.

    The controls are automatically added on two columns: labels and edits.

    Parameters
    ----------
    page : Page | None
        Owner page for controls.

        If this parameter is not known at initialization, make sure
        the attribute ``self.page`` is defined before creating any control.

    label_width : int
        Width of the first column.
    """

    def __init__(self, page: Optional[Page], label_width: int):
        self.page = page
        self.label_width = label_width
        self.controls = []

    def add_edit(self, y: int, **kwargs) -> Edit:
        """Add a :class:`Edit <ansys.scade.guitools.control.Edit>` control to the page."""
        x = kwargs.pop('x', c.LEFT_MARGIN)
        edit = Edit(self.page, x, y, _WF, **kwargs)
        self.controls.append(edit)
        return edit

    def add_static_edit(self, y: int, text: str, **kwargs) -> StaticEdit:
        """Add a :class:`StaticEdit <ansys.scade.guitools.control.StaticEdit>` control to the page."""
        wl = kwargs.pop('wl', self.label_width)
        x = kwargs.pop('x', c.LEFT_MARGIN)
        edit = StaticEdit(self.page, text, wl, x, y, _WF, **kwargs)
        self.controls.append(edit)
        return edit

    def add_file_selector(
        self, y: int, text: str, extension: str, dir: str, filter: str, mode: FSM, **kwargs
    ) -> FileSelector:
        """Add a :class:`FileSelector <ansys.scade.guitools.control.FileSelector>` to the page."""
        wl = kwargs.pop('wl', self.label_width)
        x = kwargs.pop('x', c.LEFT_MARGIN)
        file = FileSelector(
            self.page,
            text,
            extension,
            dir,
            filter,
            mode,
            wl,
            x,
            y,
            _WF,
            **kwargs,
        )
        self.controls.append(file)
        return file

    def add_check_button(self, y: int, text: str, **kwargs) -> CheckButton:
        """Add a :class:`CheckButton <ansys.scade.guitools.control.CheckButton>` control to the page."""
        x = kwargs.pop('x', c.LEFT_MARGIN)
        w = kwargs.pop('w', self.label_width)
        cb = CheckButton(self.page, text, x, y, w, **kwargs)
        self.controls.append(cb)
        return cb

    def add_combo_box(self, y: int, text: str, **kwargs) -> ComboBox:
        """Add a :class:`ComboBox <ansys.scade.guitools.control.ComboBox>` control to the page."""
        x = kwargs.pop('x', c.LEFT_MARGIN)
        cb = ComboBox(self.page, x, y, _WF, **kwargs)
        self.controls.append(cb)
        return cb

    def add_object_combo_box(self, y: int, text: str, **kwargs) -> ObjectComboBox:
        """Add a :class:`ObjectComboBox <ansys.scade.guitools.control.ObjectComboBox>` control to the page."""
        x = kwargs.pop('x', c.LEFT_MARGIN)
        cb = ObjectComboBox(self.page, x, y, _WF, **kwargs)
        self.controls.append(cb)
        return cb

    def add_static_combo_box(self, y: int, text: str, **kwargs) -> StaticComboBox:
        """Add a :class:`StaticComboBox <ansys.scade.guitools.control.StaticComboBox>` control to the page."""
        wl = kwargs.pop('wl', self.label_width)
        x = kwargs.pop('x', c.LEFT_MARGIN)
        cb = StaticComboBox(self.page, text, wl, x, y, _WF, **kwargs)
        self.controls.append(cb)
        return cb

    def add_static_object_combo_box(self, y: int, text: str, **kwargs) -> StaticObjectComboBox:
        """Add a :class:`StaticObjectComboBox <ansys.scade.guitools.control.StaticObjectComboBox>` control to the page."""
        wl = kwargs.pop('wl', self.label_width)
        x = kwargs.pop('x', c.LEFT_MARGIN)
        cb = StaticObjectComboBox(self.page, text, wl, x, y, _WF, **kwargs)
        self.controls.append(cb)
        return cb

    def add_radio_box(self, y: int, buttons: List[Tuple[Any, str]], **kwargs) -> RadioBox:
        """Add a :class:`RadioBox <ansys.scade.guitools.control.RadioBox>` control to the page."""
        x = kwargs.pop('x', c.LEFT_MARGIN)
        rb = RadioBox(self.page, buttons, x, y, _WF, **kwargs)
        self.controls.append(rb)
        return rb

    def add_group_radio_box(
        self, y: int, text: str, buttons: List[Tuple[Any, str]], **kwargs
    ) -> GroupRadioBox:
        """Add a :class:`GroupRadioBox <ansys.scade.guitools.control.GroupRadioBox>` control to the page."""
        x = kwargs.pop('x', c.LEFT_MARGIN)
        grb = GroupRadioBox(self.page, text, buttons, x, y, _WF, **kwargs)
        self.controls.append(grb)
        return grb

    def add_static_radio_box(
        self, y: int, text: str, buttons: List[Tuple[Any, str]], **kwargs
    ) -> StaticRadioBox:
        """Add a :class:`StaticRadioBox <ansys.scade.guitools.control.StaticRadioBox>` control to the page."""
        wl = kwargs.pop('wl', self.label_width)
        x = kwargs.pop('x', c.LEFT_MARGIN)
        srb = StaticRadioBox(self.page, text, wl, buttons, x, y, _WF, **kwargs)
        self.controls.append(srb)
        return srb

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

    It introduces a new abstract method that must be implemented
    for building the controls.
    """

    def __init__(self, label_width: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super(SettingsPage, self).__init__(self, label_width)
        self.ddx = None  # type: Optional[ISettingsDataExchange]

    def on_build(self):
        """Build the settings page."""
        # reset the list of controls
        self.controls = []
        self.ddx = self.on_build_ex()

    def on_layout(self):
        """Specify how controls are moved or resized."""
        self.layout_controls()

    def on_display(self, project: Project, configuration: Configuration):
        """Update the page with the properties read from the project."""
        if self.ddx:
            self.ddx.model_to_page(project, configuration)

    def on_validate(self, project: Project, configuration: Configuration):
        """Update the project with the properties read from the page."""
        if self.ddx:
            self.ddx.page_to_model(project, configuration)

    @abstractmethod
    def on_build_ex(self) -> Optional[ISettingsDataExchange]:
        """
        Build the controls and return an optional object for managing the persistence.

        Returns
        -------
        Optional[ISettingsDataExchange]
            Object for exchanging data between the project and the controls.
        """
        raise NotImplementedError


class PropertyPageEx(PropertyPage, ContainerPage):
    """
    Provides a base class for property pages.

    This class also provides means to manage the sizing
    of most common controls and their serialization.

    It introduces a new abstract method that must be implemented
    for building the controls.

    Parameters
    ----------
    label_width : int
        Width of the labels, displayed before the controls on the same line.
    """

    def __init__(self, label_width: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super(PropertyPage, self).__init__(self, label_width)
        self.ddx = None  # type: Optional[IPropertiesDataExchange]
        self.models = []  # type: List[Any]

    def on_build(self):
        """Build the properties page."""
        # reset the list of controls
        self.controls = []
        self.ddx = self.on_build_ex()

    def on_layout(self):
        """Specify how controls are moved or resized."""
        self.layout_controls()

    def on_context(self, models: List[Any]):
        """
        Declare the models the page should consider.

        Parameters
        ----------
        models : List[Any]
            List of selected objects in the IDE.
        """
        self.models = models

    def on_display(self):
        """Update the page with the properties read from the models."""
        if self.ddx:
            for model in self.models:
                self.ddx.model_to_page(model)

    def on_validate(self):
        """Update the models with the properties read from the page."""
        if self.ddx:
            for model in self.models:
                self.ddx.page_to_model(model)

    @abstractmethod
    def on_build_ex(self) -> Optional[IPropertiesDataExchange]:
        """
        Build the controls and return an optional object for managing the persistence.

        Returns
        -------
        Optional[IPropertiesDataExchange]
            Object for exchanging data between the models and the controls.
        """
        raise NotImplementedError


class GuiHostClientPage(IGuiHostClient, ContainerPage):
    """Default implementation for GuiHost pages."""

    def __init__(self, *args, **kwargs):
        super(IGuiHostClient, self).__init__(page=None, *args, **kwargs)
        self.ddx = None  # type: Optional[IPropertiesDataExchange]

    def get_selected_models(self, models: List[Any]) -> List[Any]:
        """
        Return a new list of models from the selection.

        For example, replaces selected graphical elements by their
        associated semantic ones.

        Parameters
        ----------
        models : List[Any]
            List of selected objects in the IDE.

        Returns
        -------
        List[Any]
            List of objects to consider.
        """
        return models

    def is_available(self, models: List[Any]) -> bool:
        """
        Return whether the page is available for the current selection.

        Parameters
        ----------
        models : List[Any]
            List of selected objects in the IDE.
        """
        return len(self.get_selected_models(models)) > 0

    def set_models(self, models: List[Any]):
        """
        Declare the models the page should consider.

        Parameters
        ----------
        models : List[Any]
            List of selected objects in the IDE.
        """
        self.models = self.get_selected_models(models)

    def show(self, show: bool):
        """
        Show or hide the page.

        This consists in showing or hiding the contained controls.

        Parameters
        ----------
        show : bool
            Whether the page should be shown or hidden.
        """
        self.show_controls(show)

    def on_layout(self):
        """Declare the contained control's constraints."""
        self.layout_controls()

    def on_display(self):
        """Update the page with the properties read from the models."""
        if self.ddx:
            for model in self.models:
                self.ddx.model_to_page(model)

    def on_validate(self):
        """Update the models with the properties read from the page."""
        if self.ddx:
            for model in self.models:
                self.ddx.page_to_model(model)

    def on_build(self, page: PropertyPage, y: int):
        """Build the property page."""
        # update page attribute that wasn't known at initialization
        self.page = page
        # reset the list of controls
        self.controls = []
        # build the controls
        self.ddx = self.on_build_ex(y)

    def on_close(self):
        """Perform any cleaning before the page is closed."""
        pass

    @abstractmethod
    def on_build_ex(self, y: int) -> Optional[IPropertiesDataExchange]:
        """
        Build the controls and return an optional object for managing the persistence.

        Parameters
        ----------
        y : int
            Start vertical position.

        Returns
        -------
        Optional[IPropertiesDataExchange]
            Object for exchanging data between the models and the controls.
        """
        raise NotImplementedError
