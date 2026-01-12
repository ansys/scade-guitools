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

"""
Provides default metrics for designing dialog boxes and controls.

These metrics may depend on your version of Windows or selected theme.
"""

# NC area (Non client area) of dialogs
# If the bounding box of a dialog is 200x100, its client area is 184x61
H_TITLE = 28
"""Default height of the title area of a dialog box."""
NC_TOP = H_TITLE + 3
"""Non client area top margin of a dialog box."""
NC_LEFT = 8
"""Non client area left margin of a dialog box."""
NC_RIGHT = 8
"""Non client area right margin of a dialog box."""
NC_BOTTOM = 8
"""Non client area bottom margin of a dialog box."""

DY = 30
"""Default vertical offset between 2 lines."""

RIGHT_MARGIN = 6
"""Right margin of a dialog box or page."""
LEFT_MARGIN = 6
"""Left margin of a dialog box or page."""
TOP_MARGIN = 7
"""Top margin of a dialog box or page."""
BOTTOM_MARGIN = 7
"""Bottom margin of a dialog box or page."""

BUTTON_HEIGHT = 23
"""Default height of a push button control."""
BUTTON_WIDTH = 75
"""Default width of a push button control."""

STATIC_HEIGHT = 16
"""Default height of a static control."""

EDIT_HEIGHT = 20
"""Default height of an edit control."""

# height adjusted to the edit control usually associated to this button
DOTS_HEIGHT = BUTTON_HEIGHT - 1
"""Default height of the ``...`` push button control."""
DOTS_WIDTH = 30
"""Default width of a ``...`` push button control."""

CHECK_BUTTON_HEIGHT = 20
"""Default height of a check button control."""

COMBO_BOX_HEIGHT = 130
"""Default height of a combo box control."""

RADIO_BUTTON_HEIGHT = 20
"""Default height of a radio button control."""

GROUP_RADIO_BOX_HEIGHT = RADIO_BUTTON_HEIGHT + STATIC_HEIGHT + BOTTOM_MARGIN
"""Default height of a group radio box control."""

RADIO_BOX_DY = GROUP_RADIO_BOX_HEIGHT + (DY - EDIT_HEIGHT)
"""Default vertical offset for a group radio box control."""
