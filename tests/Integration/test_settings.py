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

from ansys.scade.guitools.control import FSM, PushButton
import ansys.scade.guitools.csts as c
from ansys.scade.guitools.data import SettingsDataExchange
from ansys.scade.guitools.page import SettingsPageEx


class TestSettingsPage(SettingsPageEx):
    """Defines a sample test for the page and the layout of the controls."""

    def __init__(self):
        super().__init__(150, 'Test SettingsPageEx')

    def on_build_ex(self) -> SettingsDataExchange:
        """Build the settings page."""
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
        files = projects[0].file_refs
        paths = [_.name for _ in files]
        scb = self.add_static_combo_box(y, 'Paths')
        y += dy
        scb.set_items(sorted(paths))
        # add an object combo box control with the files
        ocb = self.add_static_object_combo_box(y, 'Files')
        y += dy
        ocb.set_items(files, paths)

        # persistence
        tool = 'TEST_GUI_TOOLS'
        ddx = SettingsDataExchange(tool)
        ddx.ddx_control(field, 'FIELD', '')
        ddx.ddx_control(file, 'FILE', '')
        ddx.ddx_control(option, 'OPTION', False)
        ddx.ddx_control(scb, 'PATH', '')
        ddx.ddx_control(ocb, 'FR', '')
        return ddx
