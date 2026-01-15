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

"""Stubs for unit tests."""

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from scade.model.project.stdproject import Configuration, Project
import scade.model.suite as suite

from ansys.scade.apitools.info.install import get_scade_properties
from ansys.scade.guitools.ide import Ide


class StubIde(Ide):
    """
    SCADE IDE instantiation for unit tests.

    This class stubs most popular functions by storing inputs so that they
    can be compared with expected data.

    It can be sub-classed for specific use-cases.
    """

    def __init__(self):
        self.project: Optional[Project] = None
        self.session: Optional[suite.Session] = None
        self._selection = []
        self.browser = None
        self.browser_items: Dict[Any, Any] = {}
        # report
        # * tab: name of active report
        # * items: list of tuples, first element is the header
        self.report_tab: str = ''
        self.report_items: List[list] = []
        # decorations
        self.decorations: list[str] = []
        self.decorated_items: Dict[suite.Object, str] = {}

    # GUI-related Python commands

    def activate(self, object_: Any):
        """Ignore the call."""
        pass

    def activate_browser(self, tab_name: str):
        """Ignore the call."""
        pass

    def activate_project(self, project_name: str):
        """Ignore the call."""
        pass

    def activate_tab(self, tab: str):
        """Ignore the call."""
        pass

    def browser_report(
        self,
        child_object: Any,
        parent_object: Any = None,
        expanded: bool = False,
        user_data: Any = None,
        name: str = '',
        icon_file: str = '',
    ):
        """Stub ``scade.browser_report``."""
        if isinstance(child_object, str):
            child = child_object
        else:
            # try some common attributes
            for att in ['name', 'pathname']:
                name = getattr(child_object, att, '')
                if name:
                    break
            else:
                name = 'anonymous'
            child = f'<{type(child_object).__name__}> {name}'
        parent = self.browser_items[parent_object]
        entry = {
            'name': child,
            'icon_file': Path(icon_file).name if icon_file else '',
            'expanded': expanded,
            'user_data': user_data,
            'children': [],
        }
        parent['children'].append(entry)
        self.browser_items[child_object] = entry

    def clear_tab(self, tab: str):
        """Ignore the call."""
        pass

    def command(
        self, extension_id: str, command_id: int, command: str = 'activate'
    ) -> Optional[str]:
        """Ignore the call."""
        return None

    def create_browser(
        self,
        name: str,
        icon_file: Optional[str] = None,
        keep: bool = False,
        callback: Callable[[Any, Any], None] = None,  # type: ignore
    ):
        """Stub ``scade.create_browser``."""
        self.browser = {
            'name': name,
            'icon': Path(icon_file).name if icon_file else '',
            'children': [],
        }
        self.browser_items = {None: self.browser}

    def create_report(self, tab_name: str, *header: Tuple[str, int, int], check: bool = False):
        """Stub ``scade.create_report``."""
        self.report_tab = tab_name
        self.report_items = [[_[0] for _ in header]]

    def get_active_configuration(self, project: Project, tool_name: str) -> Optional[Configuration]:
        """Stub ``scade.get_active_configuration``."""
        return None

    def get_active_project(self) -> Project:
        """Stub ``scade.get_active_project``."""
        assert self.project is not None  # nosec B101  # addresses linter
        return self.project

    def locate(self, locate_string: str):
        """Ignore the call."""
        pass

    def locate_ex(self, tuples: Union[List[suite.Object], List[Tuple]]):
        """Ignore the call."""
        pass

    def open_document_view(self, file_name: str):
        """Ignore the call."""
        pass

    def open_html_view(
        self,
        file: Union[str, List[str]],
        use: Optional[str] = None,
        delete: bool = False,
    ):
        """Ignore the call."""
        pass

    def open_html_in_browser(self, file_name: str):
        """Ignore the call."""
        pass

    def open_source_code_view(self, file_name: str, line: int = 1, col: int = 1):
        """Ignore the call."""
        pass

    def output_log(self, tab_name: str, command: str, path_name: str = '', separator: str = ''):
        """Ignore the call."""
        pass

    def print(
        self,
        source_object: Any,
        path_name: str,
        format: str,  # 'emf' | 'text'| 'png' | 'ps'
        rotation: int = 0,
    ):
        """Ignore the call."""
        pass

    def printer_setup(self, printer_name: str):
        """Ignore the call."""
        pass

    def print_ssl(
        self,
        scade_operator: suite.Operator,
        path_name: str,
        format: str,  # 'emf' | 'png' | 'ps'
        rotation: int = 0,
    ):
        """Ignore the call."""
        pass

    def register_decoration(self, name: str, small_icon: str, large_icon: str):
        """Stub suite.register_decoration."""
        self.decorations.append(name)

    def report(self, item: Any, *columns: str):
        """Stub ``scade.report``."""
        self.report_items.append([item] + list(columns))

    @property
    def selection(self) -> List[Any]:
        """Stub return scade.selection."""
        return self._selection

    @selection.setter
    def selection(self, selection: List[Any]):
        """Stub ``scade.selection``."""
        self._selection = selection

    def set_decoration(self, object_: suite.Object, name: str):
        """Stub suite.set_decoration."""
        # assert name in self.decorations
        self.decorated_items[object_] = name

    def set_output_tab(self, tab: str):
        """Ignore the call."""
        pass

    def set_style(self, presentation_element: suite.PresentationElement, style_name: str):
        """Ignore the call."""
        pass

    def tabput(self, tab: str, text: str):
        """Ignore the call."""
        pass

    def unset_decoration(self, object_: suite.Object):
        """Ignore the call."""
        self.decorated_items.pop(object_, None)

    def version(
        self, kind: str
    ) -> str:  # 'number' | 'folderName' | 'buildNumber' | 'endYear' | 'versionName' | 'copyright'
        """Stub ``scade.version``."""
        mapping = {
            'number': 'SCADE_STUDIO_NUMBER',
            'folderName': 'INSTALL_FOLDER',
            'buildNumber': 'BUILD_NUMBER',
            'endYear': 'COPYRIGHT_END_DATE',
            'versionName': 'RELEASE',
            'copyright': 'RELEASE_COPYRIGHT',
        }
        props = get_scade_properties()
        return props.get(mapping[kind], '<unknown>')

    # Custom Dialogs

    def message_box(
        self, name: str, message: str, style: str = 'ok', icon: str = 'information'
    ) -> int:
        """Ignore the call."""
        return 0

    def file_open(self, filter: str = '', directory: str = '') -> str:
        """Ignore the call."""
        return ''

    def file_save(
        self, file_name: str, extension: str = '', directory: str = '', filter: str = ''
    ) -> str:
        """Ignore the call."""
        return ''

    def browse_directory(self, initial_directory: str = '') -> str:
        """Ignore the call."""
        return ''

    # Callback Registration

    def register_terminate_callable(self, callable):
        """Ignore the call."""
        pass

    def register_load_model_callable(self, callable):
        """Ignore the call."""
        pass

    def register_unload_model_callable(self, callable):
        """Ignore the call."""
        pass

    # API-Related Python Commands

    def get_projects(self) -> List[Project]:
        """Stub ``scade.model.project.stdproject.get_roots``."""
        return [self.get_active_project()]

    def get_sessions(self) -> List[suite.Session]:
        """Stub ``scade.model.suite.get_roots``."""
        assert self.session is not None  # nosec B101  # addresses linter
        return [self.session]

    # Misc.

    def log(self, text: str):
        """Redirect the call to the local log function."""
        log(text)

    def save_browser(self, path: Path):
        """Store the current browser as a json file."""
        with path.open('w') as f:
            json.dump(self.browser, f, indent='   ', sort_keys=True)


def log(text: str):
    """Log the message. Temporary implementation."""
    print(text)


studio = StubIde()
