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

from scade.model.project.stdproject import FileRef

from ansys.scade.guitools.page import GuiHostClientPage


class TestGuiHostClientPage(GuiHostClientPage):
    """Base class for tests that applies to files."""

    __test__ = False

    def __init__(self, label: str, ext: str = '', **kwargs):
        super().__init__(label_width=100, **kwargs)
        self.label = label
        self.ext = ext

    def on_build_ex(self, y: int):
        """Build the controls."""
        self.ed_file = self.add_static_edit(y, self.label)

    def get_selected_models(self, models: List[Any]) -> List[Any]:
        """Filter anything but files."""
        return [_ for _ in models if isinstance(_, FileRef)]

    def is_available(self, models) -> bool:
        """Return whether the page is available for the current selection."""
        selected_models = self.get_selected_models(models)
        available = len(selected_models) > 0
        if available and self.ext:
            available = all([Path(_.pathname).suffix == self.ext for _ in selected_models])
        return available

    def on_display(self):
        """Update the page with the paths of the selected files."""
        assert self.models
        text = self.models[0].pathname if len(self.models) == 1 else '<multiple selection>'
        self.ed_file.set_name(text)


class PageTxt(TestGuiHostClientPage):
    """Property page for text files (TXT)."""

    def __init__(self):
        super().__init__('Text', '.txt')


class PageAll(TestGuiHostClientPage):
    """Property page for any files (*)."""

    def __init__(self):
        super().__init__('File')


class PagePython(TestGuiHostClientPage):
    """Property page for Python files (PY)."""

    def __init__(self):
        super().__init__('Python', '.py')
