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

"""Test extension Ansys SCADE GUI Tools."""

from scade.model.project.stdproject import get_roots as get_projects
from scade.tool.suite.gui.commands import Command

from ansys.scade.guitools.control import (
    FSM,
    CheckButton,
    FileSelector,
    GroupRadioBox,
    PushButton,
    RadioBox,
    StaticComboBox,
    StaticEdit,
    StaticObjectComboBox,
    StaticRadioBox,
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
        super().__init__('TestControl', 400, 430, style=DS.CLOSE)

    def on_build_ex(self):
        """Build the dialog."""
        x = c.LEFT_MARGIN
        y = c.TOP_MARGIN
        dy = c.DY
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
        self.fs = _TestFileSelector(self, 'File', '.py', '', filter, FSM.OPEN, wl, x, y, w)
        y += dy
        # add a check button
        CheckButton(self, 'Hide FileSelector', x, y, wl, on_click=self.on_click_check)
        y += dy
        # add a directory selector
        self.ds = _TestFileSelector(self, 'Directory', '', '', '', FSM.DIR, wl, x, y, w)
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
        # can't use dy here, get the vertical margin from other xontrol)
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
        # add a group radio box with two buttons
        grb = GroupRadioBox(self, 'Radio box', [('1', '&First'), ('2', '&Second')], x, y, w)
        grb.set_value('2')
        y += c.RADIO_BOX_DY
        # add a static radio box with three buttons
        srb = StaticRadioBox(
            self, 'Buttons', wl, [('One', '&One'), ('Two', 'T&wo'), ('Three', '&Three')], x, y, w
        )
        # select one value
        srb.set_value('One')
        # and make sure everything can be unselected, for example for multiple selection management
        srb.set_value('')
        y += dy
        # add a radio box with one button
        rb = RadioBox(self, [('SINGLE', '&Button')], x, y, w)
        rb.set_value('<UNKNOWN>')
        y += dy

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
