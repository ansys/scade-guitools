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

"""``Ide`` interface implementation."""

# this module uses `type: ignore` pragmas for ``scade`` functions: they
# are defined dynamically when the interpreter is created: typing analysis
# is not possible

# from collections.abc import Callable
from typing import Any, Callable, List, Optional, Tuple, Union

import scade
from scade.model import suite
from scade.model.project.stdproject import Configuration, Project, get_roots as get_projects
from scade.model.suite import get_roots as get_sessions

from ansys.scade.apitools import print
from ansys.scade.guitools.ide import Ide


class Studio(Ide):
    """Implementation for SCADE IDE."""

    # GUI-related Python commands

    def activate(self, object_: Any):
        """Redirect the call to SCADE IDE."""
        scade.activate(object_)  # type: ignore

    def activate_browser(self, tab_name: str):
        """Redirect the call to SCADE IDE."""
        scade.activate_browser(tab_name)  # type: ignore

    def activate_project(self, project_name: str):
        """Redirect the call to SCADE IDE."""
        scade.activate_project(project_name)  # type: ignore

    def activate_tab(self, tab: str):
        """Redirect the call to SCADE IDE."""
        scade.activate_tab(tab)  # type: ignore

    def browser_report(
        self,
        child_object: Any,
        parent_object: Any = None,
        expanded: bool = False,
        user_data: Any = None,
        name: str = '',
        icon_file: str = '',
    ):
        """Redirect the call to SCADE IDE."""
        # issue with 'icon_file' default value (2025 R2)
        if icon_file:
            scade.browser_report(child_object, parent_object, expanded, user_data, name, icon_file)  # type: ignore
        else:
            scade.browser_report(child_object, parent_object, expanded, user_data, name)  # type: ignore

    def clear_tab(self, tab: str):
        """Redirect the call to SCADE IDE."""
        scade.clear_tab(tab)  # type: ignore

    def command(
        self, extension_id: str, command_id: int, command: str = 'activate'
    ) -> Optional[str]:
        """Redirect the call to SCADE IDE."""
        # dynamic and undisclosed API
        return scade.command(extension_id, command_id, command)  # type: ignore reportAttributeAccessIssue

    def create_browser(
        self,
        name: str,
        icon_file: Optional[str] = None,
        keep: bool = False,
        callback: Callable[[Any, Any], None] = None,  # type: ignore
    ):
        """Redirect the call to SCADE IDE."""
        # issue with 'icon_file' default value (2025 R2)
        if icon_file:
            scade.create_browser(name, icon_file, keep, callback)  # type: ignore
        else:
            scade.create_browser(name, keep=keep, callback=callback)  # type: ignore

    def create_report(self, tab_name: str, *header: Tuple[str, int, int], check: bool = False):
        """Redirect the call to SCADE IDE."""
        scade.create_report(tab_name, *header, check)  # type: ignore

    def get_active_configuration(self, project: Project, tool_name: str) -> Optional[Configuration]:
        """Redirect the call to SCADE IDE."""
        return scade.get_active_configuration(project, tool_name)

    def get_active_project(self) -> Project:
        """Redirect the call to SCADE IDE."""
        return scade.get_active_project()  # type: ignore

    def locate(self, locate_string: str):
        """Redirect the call to SCADE IDE."""
        scade.locate(locate_string)  # type: ignore

    def locate_ex(self, tuples: Union[List[suite.Object], List[Tuple]]):
        """Redirect the call to the API."""
        suite.locate(tuples)  # type: ignore

    def open_document_view(self, file_name: str):
        """Redirect the call to SCADE IDE."""
        scade.open_document_view(file_name)  # type: ignore

    def open_html_view(
        self,
        file: Union[str, List[str]],
        use: Optional[str] = None,
        delete: bool = False,
    ):
        """Redirect the call to SCADE IDE."""
        scade.open_html_view(file, use, delete)  # type: ignore

    def open_html_in_browser(self, file_name: str):
        """Redirect the call to SCADE IDE."""
        scade.open_html_in_browser(file_name)  # type: ignore

    def open_source_code_view(self, file_name: str, line: int = 1, col: int = 1):
        """Redirect the call to SCADE IDE."""
        scade.open_source_code_view(file_name, line, col)  # type: ignore

    def output_log(
        self,
        tab_name: str,
        command: str,  # 'on' | 'off'
        path_name: str = '',
        separator: str = '',
    ):
        """Redirect the call to SCADE IDE."""
        scade.output_log(tab_name, command, path_name, separator)  # type: ignore

    def print(
        self,
        source_object: Any,
        path_name: str,
        format: str,  # 'emf' | 'text'| 'png' | 'ps'
        rotation: int = 0,
    ):
        """Redirect the call to SCADE IDE."""
        scade.print(source_object, path_name, format, rotation)

    def printer_setup(self, printer_name: str):
        """Redirect the call to SCADE IDE."""
        scade.printer_setup(printer_name)  # type: ignore

    def print_ssl(
        self,
        scade_operator: suite.Operator,
        path_name: str,
        format: str,  # 'emf' | 'png' | 'ps'
        rotation: int = 0,
    ):
        """Redirect the call to the API."""
        suite.print_ssl(scade_operator, path_name, format, rotation)

    def register_decoration(self, name: str, small_icon: str, large_icon: str):
        """Redirect the call to the API."""
        # function defined at runtime
        suite.register_decoration(name, str(small_icon), str(large_icon))  # type: ignore

    def report(self, item: Any, *columns: str):
        """Redirect the call to SCADE IDE."""
        scade.report(item, *columns)  # type: ignore

    @property
    def selection(self) -> List[Any]:
        """Redirect the call to SCADE IDE."""
        return scade.selection  # type: ignore

    @selection.setter
    def selection(self, selection: List[Any]):
        """Stub ``scade.selection``."""
        scade.selection = selection

    def set_decoration(self, object_: suite.Object, name: str):
        """Redirect the call to the API."""
        # function defined at runtime
        suite.set_decoration(object_, name)  # type: ignore

    def set_output_tab(self, tab: str):
        """Redirect the call to SCADE IDE."""
        scade.set_output_tab(tab)  # type: ignore

    def set_style(self, presentation_element: suite.PresentationElement, style_name: str):
        """Redirect the call to the API."""
        suite.set_style(presentation_element, style_name)

    def tabput(self, tab: str, text: str):
        """Redirect the call to SCADE IDE."""
        scade.tabput(tab, text)  # type: ignore

    def unset_decoration(self, object_: suite.Object):
        """Redirect the call to the API."""
        # function defined at runtime
        suite.unset_decoration(object_)  # type: ignore

    def version(
        self,
        kind: str,  # 'number' | 'folderName' | 'buildNumber' | 'endYear' | 'versionName' | 'copyright'
    ) -> str:
        """Redirect the call to SCADE IDE."""
        return scade.version(kind)  # type: ignore

    # Custom Dialogs

    def message_box(
        self, name: str, message: str, style: str = 'ok', icon: str = 'information'
    ) -> int:
        """Stub ``scade.tool.suite.gui.dialogs.message_box``."""
        return 0

    def file_open(self, filter: str = '', directory: str = '') -> str:
        """Stub ``scade.tool.suite.gui.dialogs.file_open``."""
        return ''

    def file_save(
        self, file_name: str, extension: str = '', directory: str = '', filter: str = ''
    ) -> str:
        """Stub ``scade.tool.suite.gui.dialogs.file_save``."""
        return ''

    def browse_directory(self, initial_directory: str = '') -> str:
        """Stub ``scade.tool.suite.gui.dialogs.browse_directory``."""
        return ''

    # Callback Registration

    def register_terminate_callable(self, callable):
        """Stub ``scade.tool.suite.gui.register_terminate_callable``."""
        pass

    def register_load_model_callable(self, callable):
        """Stub ``scade.tool.suite.gui.register_load_model_callable``."""
        pass

    def register_unload_model_callable(self, callable):
        """Stub ``scade.tool.suite.gui.register_unload_model_callable``."""
        pass

    # API-Related Python Commands

    def get_projects(self) -> List[Project]:
        """Redirect the call to the API."""
        return get_projects()

    def get_sessions(self) -> List[suite.Session]:
        """Redirect the call to the API."""
        return get_sessions()

    # Misc.

    def log(self, text: str):
        """Redirect the call to the local log function."""
        log(text)


def log(text: str):
    """Log the message. Temporary implementation."""
    print(text)


studio = Studio()
