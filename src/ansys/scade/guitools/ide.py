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

"""SCADE IDE abstraction."""

from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional, Tuple, Union

from scade.model import suite
from scade.model.project.stdproject import Configuration, Project


class Ide(ABC):
    """SCADE IDE abstraction."""

    # GUI-related Python commands

    @abstractmethod
    def activate(self, object_: Any):
        """Abstract ``scade.activate``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def activate_browser(self, tab_name: str):
        """Abstract ``scade.activate_browser``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def activate_project(self, project_name: str):
        """Abstract ``scade.activate_project``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def activate_tab(self, tab: str):
        """Abstract ``scade.activate_tab``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def browser_report(
        self,
        child_object: Any,
        parent_object: Any = None,
        expanded: bool = False,
        user_data: Any = None,
        name: str = '',
        icon_file: str = '',
    ):
        """Abstract ``scade.browser_report``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def clear_tab(self, tab: str):
        """Abstract ``scade.clear_tab``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def command(
        self, extension_id: str, command_id: int, command: str = 'activate'
    ) -> Optional[str]:
        """Abstract ``scade.command (undocumented API)``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def create_browser(
        self,
        name: str,
        icon_file: Optional[str] = None,
        keep: bool = False,
        callback: Callable[[Any, Any], None] = None,
    ):
        """Abstract ``scade.create_browser``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def create_report(self, tab_name: str, *header: Tuple[str, int, int], check: bool = False):
        """Abstract ``scade.create_report``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def get_active_configuration(self, project: Project, tool_name: str) -> Optional[Configuration]:
        """Abstract ``scade.get_active_configuration``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def get_active_project(self) -> Optional[Project]:
        """Abstract ``scade.get_active_project``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def locate(self, locate_string: str):
        """Abstract ``scade.locate``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def locate_ex(self, tuples: Union[List[suite.Object], List[Tuple]]):
        """Abstract ``scade.model.suite.locate``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def open_document_view(self, file_name: str):
        """Abstract ``scade.open_document_view``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def open_html_view(
        self,
        file: Union[str, List[str]],
        use: Optional[str] = None,
        delete: bool = False,
    ):
        """Abstract ``scade.open_html_view``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def open_html_in_browser(self, file_name: str):
        """Abstract ``scade.open_html_in_browser``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def open_source_code_view(self, file_name: str, line: int = 1, col: int = 1):
        """Abstract ``scade.open_source_code_view``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def output_log(
        self,
        tab_name: str,
        command: str,  # 'on' | 'off'
        path_name: str = '',
        separator: str = '',
    ):
        """Abstract ``scade.output_log``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def print(
        self,
        source_object: Any,
        path_name: str,
        format: str,  # 'emf' | 'text'| 'png' | 'ps'
        rotation: int = 0,
    ):
        """Abstract ``scade.print``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def printer_setup(self, printer_name: str):
        """Abstract ``scade.printer_setup``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def print_ssl(
        self,
        scade_operator: suite.Operator,
        path_name: str,
        format: str,  # 'emf' | 'png' | 'ps'
        rotation: int = 0,
    ):
        """Abstract ``scade.model.suite.print_ssl``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def register_decoration(self, name: str, small_icon: str, large_icon: str):
        """Abstract ``scade.model.suite.register_decoration``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def report(self, item: Any, *columns: str):
        """Abstract ``scade.report``."""
        raise NotImplementedError('Abstract method call')

    @property
    @abstractmethod
    def selection(self) -> List[Any]:
        """Abstract ``scade.selection``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def set_decoration(self, object_: suite.Object, name: str):
        """Abstract ``scade.model.suite.set_decoration``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def set_output_tab(self, tab: str):
        """Abstract ``scade.set_output_tab``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def set_style(self, presentation_element: suite.PresentationElement, style_name: str):
        """Abstract ``scade.model.suite.set_style``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def tabput(self, tab: str, text: str):
        """Abstract ``scade.tabput``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def unset_decoration(self, object_: suite.Object):
        """Abstract ``scade.model.suite.set_decoration``."""
        raise NotImplementedError('Abstract method call')

    @property
    @abstractmethod
    def version(
        self, kind: str
    ) -> str:  # 'number' | 'folderName' | 'buildNumber' | 'endYear' | 'versionName' | 'copyright'
        """Abstract ``scade.version``."""
        raise NotImplementedError('Abstract method call')

    # Custom Dialogs

    @abstractmethod
    def message_box(
        self, name: str, message: str, style: str = 'ok', icon: str = 'information'
    ) -> int:
        """Abstract ``scade.tool.suite.gui.dialogs.message_box``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def file_open(self, filter: str = '', directory: str = '') -> str:
        """Abstract ``scade.tool.suite.gui.dialogs.file_open``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def file_save(
        self, file_name: str, extension: str = '', directory: str = '', filter: str = ''
    ) -> str:
        """Abstract ``scade.tool.suite.gui.dialogs.file_save``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def browse_directory(self, initial_directory: str = '') -> str:
        """Abstract ``scade.tool.suite.gui.dialogs.file_save``."""
        raise NotImplementedError('Abstract method call')

    # Callback Registration

    @abstractmethod
    def register_terminate_callable(self, callable):
        """Abstract ``scade.tool.suite.gui.register_terminate_callable``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def register_load_model_callable(self, callable):
        """Abstract ``scade.tool.suite.gui.register_load_model_callable``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def register_unload_model_callable(self, callable):
        """Abstract ``scade.tool.suite.gui.register_unload_model_callable``."""
        raise NotImplementedError('Abstract method call')

    # API-Related Python Commands

    @abstractmethod
    def get_projects(self) -> List[Project]:
        """Abstract ``scade.model.project.stdproject.get_roots``."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def get_sessions(self) -> List[suite.Session]:
        """Abstract ``scade.model.suite.get_roots``."""
        raise NotImplementedError('Abstract method call')

    # Misc.

    @abstractmethod
    def log(self, text: str):
        """Abstract ``scade.output``."""
        raise NotImplementedError('Abstract method call')
