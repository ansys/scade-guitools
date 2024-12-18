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

"""Test extension Ansys SCADE GUI Tools."""

from pathlib import Path

from scade.model.project.stdproject import get_roots as get_projects

from ansys.scade.guitools.control import FSM, FileSelector, PushButton
import ansys.scade.guitools.csts as c
from ansys.scade.guitools.page import SettingsPageEx


class _TestFileSelector(FileSelector):
    """Hooks on_click."""

    __test__ = False

    def on_click(self, *args):
        """Set the directory and reference attributes from the test dialog."""
        self.directory = self.owner.ed_directory.get_name()
        self.reference = self.owner.ed_reference.get_name()
        super().on_click(*args)


class TestSettingsPage(SettingsPageEx):
    """Defines a sample test for the page and the layout of the controls."""

    def __init__(self):
        super().__init__(150, 'Test SettingsPageEx')

        # for get/set functions
        self.ocb = None
        self.files = []

    def on_build(self):
        """Build the settings page."""
        # call the base class' method: mandatory
        super().on_build()

        # alignment for the first line
        y = c.TOP_MARGIN
        dy = 30

        # add a push button
        pb = PushButton(self, 'PushButton', c.LEFT_MARGIN, y)
        self.controls.append(pb)
        y += dy
        # add a static + edit
        field = self.add_static_edit(y, 'Field')
        y += dy
        # add a file selector
        filter = 'Python files (*.py)|*.py|All Files (*.*)|*.*||'
        reference = str(Path(__file__).parent)
        file = self.add_file_selector(y, 'File', '.py', '', filter, FSM.OPEN, reference=reference)
        y += dy
        # add a check button
        option = self.add_check_button(y, 'Option')
        y += dy
        # add a combo box control with the name of the files
        projects = get_projects()
        self.files = projects[0].file_refs
        paths = sorted([_.name for _ in self.files])
        scb = self.add_static_combo_box(y, 'Paths')
        y += dy
        scb.set_items(paths)
        # add an object combo box control with the files
        self.ocb = self.add_static_object_combo_box(y, 'Files')
        y += dy
        self.ocb.set_items(self.files)

        # properties
        tool = 'TEST_GUI_TOOLS'
        self.declare_property(field.get_name, field.set_name, tool, 'FIELD', '')
        self.declare_property(file.get_name, file.set_name, tool, 'FILE', '')
        self.declare_property(option.get_check, option.set_check, tool, 'OPTION', False)
        self.declare_property(scb.get_name, scb.set_name, tool, 'PATH', '')
        # use dedicated handlers
        self.declare_property(self.ocb.get_name, self.ocb_set_selection, tool, 'FR', '')

    def ocb_set_selection(self, name: str):
        assert self.ocb
        for file in self.files:
            if file.name == name:
                break
        else:
            file = None  # self.files[0]
        self.ocb.set_selection(file)
