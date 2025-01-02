# -*- coding: utf-8 -*-

# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
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

from scade.model.project.stdproject import get_roots as get_projects
from scade.tool.suite.gui.commands import Command

from ansys.scade.guitools.control import (
    FSM,
    CheckButton,
    FileSelector,
    PushButton,
    StaticComboBox,
    StaticEdit,
    StaticObjectComboBox,
)
import ansys.scade.guitools.csts as c
from ansys.scade.guitools.dialog import DS, DialogBox


class _TestFileSelector(FileSelector):
    """Hooks on_click."""

    __test__ = False

    def on_click(self, *args):
        """Set the directory and reference attributes from the test dialog."""
        self.directory = self.owner.ed_directory.get_name()
        self.reference = self.owner.ed_reference.get_name()
        super().on_click(*args)


class _TestControl(DialogBox):
    """Defines a sample dialog box to test the controls."""

    __test__ = False

    def __init__(self):
        super().__init__('TestControl', 400, 300, style=DS.CLOSE)

    def on_build(self):
        """Build the dialog."""
        super().on_build()
        x = c.LEFT_MARGIN
        y = c.TOP_MARGIN
        dy = 30
        wl = 150
        w = self.right - c.LEFT_MARGIN - c.RIGHT_MARGIN
        # add a push button
        PushButton(self, 'PushButton', x, y)
        y += dy
        # add a static + edit
        StaticEdit(self, 'Static', wl, x, y, w, name='Edit')
        y += dy
        # add a file selector
        self.ed_directory = StaticEdit(self, 'Directory', wl, x, y, w, name='$(SCADE)/scripts')
        y += dy
        self.ed_reference = StaticEdit(self, 'Reference', wl, x, y, w)
        y += dy
        filter = 'Python files (*.py)|*.py|All Files (*.*)|*.*||'
        self.fs = _TestFileSelector(self, 'Static', '.py', '', filter, FSM.OPEN, wl, x, y, w)
        y += dy
        # add a check button
        CheckButton(self, 'Hide FileSelector', x, y, wl, on_click=self.on_click_check)
        y += dy
        # add a combo box control with the name of the files
        projects = get_projects()
        if projects:
            files = projects[0].file_refs
            paths = sorted([_.name for _ in files])
        else:
            files = []
            paths = []
        scb = StaticComboBox(self, 'Paths', wl, x, y, w)
        y += dy
        scb.set_items(paths)
        if paths:
            scb.set_selection(paths[0])
        # add an object combo box control with the files
        ocb = StaticObjectComboBox(self, 'Files', wl, x, y, w)
        y += dy
        ocb.set_items(files)
        if files:
            ocb.set_selection(files[0])

    def on_click_check(self, button):
        self.fs.set_visible(not button.get_check())


class CommandTestControl(Command):
    """Defines a command to display a dialog box."""

    def __init__(self):
        label = 'Control'
        super().__init__(name=f'&{label}...', status_message=label, tooltip_message=label)

    def on_activate(self):
        """Open the dialog."""
        _TestControl().do_modal()
