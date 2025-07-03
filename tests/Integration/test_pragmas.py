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

from typing import Any, List

import scade.model.suite as suite

import ansys.scade.guitools.csts as c
from ansys.scade.guitools.data import ScadePropertiesDataExchange
from ansys.scade.guitools.page import PropertyPageEx


class TestPragmaPropertyPage(PropertyPageEx):
    """Defines a sample test for the persistence as pragmas."""

    def __init__(self):
        super().__init__(50, 'Test Pragma')

    def on_build_ex(self) -> ScadePropertiesDataExchange:
        """Build the property page with a few controls."""
        # alignment for the first line
        y = c.TOP_MARGIN

        # add a static + edit
        target = self.add_static_edit(y, '&Target name:')
        y += c.DY
        # add a static + edit
        id = self.add_static_edit(y, '&Id:')
        y += c.DY
        # add a check button
        sync = self.add_check_button(y, '&Synchronize:')
        y += c.DY
        # add radio buttons
        color = self.add_static_radio_box(
            y, '&Color', [('blue', '&Blue'), ('white', '&White'), ('red', '&Red')]
        )
        y += c.DY

        # serialization
        pp = ScadePropertiesDataExchange('test_guitools')
        pp.ddx_control(target, 'target', '', '<target name>')
        pp.ddx_control(id, 'id', '9')
        pp.ddx_control(sync, 'sync', False)
        pp.ddx_control(color, 'color', 'blue')
        return pp

    def is_available(self, models: List[Any]) -> bool:
        """Return whether the page is available for the current selection."""
        return len(models) == 1 and isinstance(models[0], suite.Package)
