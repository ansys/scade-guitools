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

"""Interfaces for GUI Host pages and data persistence."""

from abc import ABC, abstractmethod
from typing import Any, List

from scade.model.project.stdproject import Configuration, Project
from scade.tool.suite.gui.properties import Page as PropertyPage


class ISettingsDataExchange(ABC):
    """Interface for exchanging data between a settings page and the model."""

    @abstractmethod
    def model_to_page(self, project: Project, configuration: Configuration):
        """
        Update the page with the properties read from the project for a given configuration.

        Parameters
        ----------
        project : Project
            Input Project.

        configuration : Configuration
            Input configuration.
        """
        raise NotImplementedError

    @abstractmethod
    def page_to_model(self, project: Project, configuration: Configuration):
        """
        Update the project with the properties read from the page for a given configuration.

        Parameters
        ----------
        project : Project
            Input Project.

        configuration : Configuration
            Input configuration.
        """
        raise NotImplementedError


class IPropertiesDataExchange(ABC):
    """Interface for exchanging data between a property page and the model."""

    @abstractmethod
    def model_to_page(self, model: Any):
        """
        Update the page with the properties read from the model.

        Parameters
        ----------
        model : Any
            Selected model element.
        """
        raise NotImplementedError

    @abstractmethod
    def page_to_model(self, model: Any):
        """
        Update the model with the properties read from the page.

        Parameters
        ----------
        model : Any
            Selected model element.
        """
        raise NotImplementedError


class IGuiHostClient(ABC):
    """Defines the interface for hosted pages."""

    @abstractmethod
    def is_available(self, models: List[Any]) -> bool:
        """
        Return whether the page is available for the current selection.

        Parameters
        ----------
        models : List[Any]
            List of selected objects in the IDE.
        """
        raise NotImplementedError

    @abstractmethod
    def set_models(self, models: List[Any]):
        """
        Declare the models the page should consider.

        Parameters
        ----------
        models : List[Any]
            List of selected objects in the IDE.
        """
        raise NotImplementedError

    @abstractmethod
    def on_build(self, page: PropertyPage, y: int) -> int:
        """
        Build the controls.

        Parameters
        ----------
        page : PropertyPage
            Owning property page, to create controls.

        y : int
            Start vertical position.
        """
        raise NotImplementedError

    @abstractmethod
    def show(self, show: bool):
        """
        Show or hide the page.

        This consists in showing or hiding the contained controls.

        Parameters
        ----------
        show : bool
            Whether the page should be shown or hidden.
        """
        raise NotImplementedError

    @abstractmethod
    def on_layout(self):
        """Declare the contained control's constraints."""
        raise NotImplementedError

    @abstractmethod
    def on_display(self):
        """Update the page with the properties read from the models."""
        raise NotImplementedError

    @abstractmethod
    def on_validate(self):
        """Update the models with the properties read from the page."""
        raise NotImplementedError

    @abstractmethod
    def on_close(self):
        """Perform any cleaning before the page is closed."""
        raise NotImplementedError
