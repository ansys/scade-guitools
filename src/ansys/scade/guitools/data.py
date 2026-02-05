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

"""Provides extensions for the persistence of settings and properties."""

from typing import (
    Any,
    Callable,
    List,  # noqa: F401  # used in a typing annotation
    Optional,
    Tuple,
)

from scade.model.project.stdproject import Configuration, Project, ProjectEntity
import scade.model.suite as suite
from scade.tool.suite.gui.widgets import CheckBox, EditBox, ListBox, RadioButton, Widget

from ansys.scade.apitools.prop import get_pragma_json, set_pragma_json
from ansys.scade.guitools.control import ComboBox, ObjectComboBox, RadioBox
from ansys.scade.guitools.interfaces import IPropertiesDataExchange, ISettingsDataExchange

Getter = Callable[[], Any]
"""Signature for getting control value."""
Setter = Callable[[Any], None]
"""Signature for setting control value."""


class DataExchange:
    """Base class for accessing controls data."""

    def __init__(self):
        """Initialize the data exchange instance."""
        # get, set, name, default, empty
        self.properties = []  # type: List[Tuple[Getter, Setter, str, Any, Any]]

    def get_control_accessors(self, control: Widget) -> Tuple[Optional[Getter], Optional[Setter]]:
        """
        Return the get and set accessors for a control, or None if not applicable.

        Override this method in a derived class to define custom
        implementation for not supported controls.

        Parameters
        ----------
        control : Widget
            Input control.

        Returns
        -------
        tuple[Getter, Setter]
        """
        if isinstance(control, EditBox):
            return (control.get_name, control.set_name)
        elif isinstance(control, CheckBox):
            return (control.get_check, control.set_check)
        elif isinstance(control, RadioButton):
            return (control.get_check, control.set_check)
        elif isinstance(control, ComboBox):
            return (control.get_name, control.set_name)
        elif isinstance(control, ListBox):
            return (control.get_selection, control.set_selection)
        elif isinstance(control, ObjectComboBox):
            return (control.get_selected_name, control.select_name)
        elif isinstance(control, RadioBox):
            return (control.get_value, control.set_value)
        # TODO(Jean Henry): keep or remove logic
        # https://github.com/ansys/scade-guitools/issues/26
        # elif isinstance(control, ObjectListBox):
        #     return (control.get_selected_names, control.select_names)

        return None, None

    def ddx_control(self, control: Widget, name: str, default: Any, empty: Any = None):
        """
        Declare a property for automatic serialization.

        When the page is displayed, the control is updated with the value read from the model.
        When the page is validated, the model is updated with the value read from the control.

        Parameters
        ----------
        control : Widget
            Control associated to the property.

        name :
            Name of the property.

        default : Any
            Default value of the property.

        empty : Any | None
            Value to display when it is empty, default ``default``.

        Examples
        --------

        .. code-block::

            # on_build_ex method of a page
            self.tp = ToolPropDataExchange('MY_TOOL')
            ...
            edit = self.add_edit(y)
            self.tp.ddx_control(edit, name='MY_PROP', default='')
            y += csts.DY
            cb = self.add_check_button(y, 'Option')
            self.tp.ddx_control(cb, name='MY_OPTION', default=False)
            y += csts.DY
        """
        pfnget, pfnset = self.get_control_accessors(control)
        if pfnget:
            assert pfnset is not None  # nosec B101  # addresses linter
            if empty is None:
                empty = default
            self.properties.append((pfnget, pfnset, name, default, empty))


class ToolPropDataExchange(DataExchange):
    """
    Means to serialize values as project *tool properties*.

    A *tool property* is a project property which name has the following syntax:
    ``@<TOOL>:<NAME>``, where ``<TOOL>`` is a name for discriminating homonymous
    properties and ``<NAME>`` is the name of the property.

    For example: ``@GENERATOR:TARGET_DIR``

    Parameters
    ----------
    tool : str
        Name of the tool to build the project property's name: first token after ``@``.
    """

    def __init__(self, tool: str):
        """Initialize the tool property data exchange instance."""
        super().__init__()
        self.tool = tool

    def display(self, project: Project, configuration: Optional[Configuration]):
        """Update the page with the properties read from the model."""
        for _, pfnset, name, default, empty in self.properties:
            if isinstance(default, list):
                value = project.get_tool_prop_def(self.tool, name, default, configuration)
            elif isinstance(default, bool):
                value = project.get_bool_tool_prop_def(self.tool, name, default, configuration)
            else:
                # assume a scalar value
                value = project.get_scalar_tool_prop_def(self.tool, name, default, configuration)
            if not value and empty:
                value = empty
            pfnset(value)

    def validate(self, project: Project, configuration: Optional[Configuration]):
        """Update the model with the properties read from the page."""
        for pfnget, _, name, default, empty in self.properties:
            value = pfnget()
            if value == empty:
                value = default
            if isinstance(default, list):
                project.set_tool_prop_def(self.tool, name, value, default, configuration)
            elif isinstance(value, bool):
                project.set_bool_tool_prop_def(self.tool, name, value, default, configuration)
            else:
                # assume a scalar value
                project.set_scalar_tool_prop_def(self.tool, name, value, default, configuration)


class SettingsDataExchange(ISettingsDataExchange, ToolPropDataExchange):
    """Default implementation to manage the persistence of most usual controls in the project."""

    def __init__(self, tool: str):
        """Initialize the settings data exchange instance."""
        super().__init__(tool)
        # super(IPropertiesDataExchange, self).__init__(self, tool)

    def model_to_page(self, project: Project, configuration: Configuration):
        """Update the page with the properties read from the model."""
        self.display(project, configuration)

    def page_to_model(self, project: Project, configuration: Configuration):
        """Update the model with the properties read from the page."""
        self.validate(project, configuration)


class ProjectPropertiesDataExchange(IPropertiesDataExchange, ToolPropDataExchange):
    """Default implementation to manage the persistence of most usual controls in the project."""

    def __init__(self, tool: str):
        """Initialize the project properties data exchange instance."""
        super().__init__(tool)
        # super(IPropertiesDataExchange, self).__init__(self, tool)

    def model_to_page(self, model: ProjectEntity):
        """Update the page with the properties read from the model."""
        self.display(model, None)

    def page_to_model(self, model: ProjectEntity):
        """Update the model with the properties read from the page."""
        self.validate(model, None)


class PragmaDataExchange(DataExchange):
    """
    Means to serialize values as SCADE Suite pragmas.

    SCADE Suite pragmas are either text or XML. This class
    uses a textual pragma made of a json string.

    Parameters
    ----------
    id : str
        Identifier of the pragma.
    """

    def __init__(self, id: str):
        """Initialize the pragma data exchange instance."""
        super().__init__()
        self.id = id

    def display(self, object_: suite.Annotable):
        """Update the page with the properties read from the model."""
        data = get_pragma_json(object_, self.id)
        if data is None:
            # defensive programming, json syntax error error not expected
            # assert False
            return
        assert isinstance(data, dict)  # nosec B101  # addresses linter
        for _, pfnset, name, default, empty in self.properties:
            value = data.get(name, default)
            if not value and empty:
                value = empty
            pfnset(value)

    def validate(self, object_: suite.Annotable):
        """Update the model with the properties read from the page."""
        data = {}
        for pfnget, _, name, default, empty in self.properties:
            value = pfnget()
            if value == empty:
                value = default
            if value != default:
                data[name] = value
        set_pragma_json(object_, self.id, data)


class ScadePropertiesDataExchange(IPropertiesDataExchange, PragmaDataExchange):
    """Default implementation to manage the persistence of most usual controls in the model."""

    def __init__(self, id: str):
        """Initialize the SCADE properties data exchange instance."""
        super().__init__(id)
        # super(IPropertiesDataExchange, self).__init__(self, id)

    def model_to_page(self, object_: suite.Annotable):
        """Update the page with the properties read from the model element."""
        self.display(object_)

    def page_to_model(self, object_: suite.Annotable):
        """Update the model element with the properties read from the page."""
        self.validate(object_)
