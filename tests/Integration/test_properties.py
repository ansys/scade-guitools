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
from typing import Any, List

from scade.model.project.stdproject import Project

from ansys.scade.guitools.control import FSM, PushButton
import ansys.scade.guitools.csts as c
from ansys.scade.guitools.data import ProjectPropertiesDataExchange
from ansys.scade.guitools.page import PropertyPageEx


class TestPropertyPage(PropertyPageEx):
    """Defines a sample test for the page and the layout of the controls."""

    __test__ = False

    def __init__(self):
        super().__init__(50, 'Test PropertyPageEx')

    def on_build_ex(self) -> ProjectPropertiesDataExchange:
        """Build the property page with a few controls."""
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
        fs = self.add_file_selector(y, 'File', '.py', '', filter, FSM.OPEN, reference=reference)
        y += dy

        # serialization
        pp = ProjectPropertiesDataExchange('MY_TOOL')
        pp.ddx_control(field, 'MY_FIELD', '')
        pp.ddx_control(fs, 'MY_FILTER', '')
        return pp

    def is_available(self, models: List[Any]) -> bool:
        """Return whether the page is available for the current selection."""
        return len(models) == 1 and isinstance(models[0], Project)
