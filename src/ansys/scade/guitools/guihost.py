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

"""Provides access to GUI server for property pages."""

import traceback
from typing import Any, Dict, List

import scade

from ansys.scade.apitools.info import get_scade_version
from ansys.scade.guitools import __version__, importlib_metadata
from ansys.scade.guitools.control import ComboBox
import ansys.scade.guitools.csts as c
from ansys.scade.guitools.interfaces import IGuiHostClient
from ansys.scade.guitools.page import PropertyPageEx

_pages = {}


class ProxyPageClient:
    """
    Maintains a reference to a client page and the name of its category.

    Parameters
    ----------
    category : str
        Name of the page.

    client : IGuiHostClient
        Instance of the hosted page.
    """

    def __init__(self, category: str, client: IGuiHostClient):
        """Initialize the proxy with a category and a client."""
        self.category = category
        self.client = client


class HostPage(PropertyPageEx):
    """
    Defines a property page for hosting client pages.

    Parameters
    ----------
    name : str
        Name of the property Page.

    optional : bool
        Whether the combo box for selecting clients is hidden
        when there is only one client.

    args : Any
        Additional parameters for the property page.

    kwargs : Any
        Additional parameters for the property page.
    """

    def __init__(self, name: str, optional: bool, *args, **kwargs):
        """Initialize the host page."""
        super().__init__(50, name=name, *args, **kwargs)
        self.optional = optional

        # registered clients
        self.proxies: List[ProxyPageClient] = []
        # active clients for the current selection, indexed by category
        self.active_clients: Dict[str, ProxyPageClient] = {}
        # active categories (sorted)
        self.categories: List[str] = []
        # current selected category
        self.category = ''
        # controls
        self.cb_clients = None

    def add_client(self, proxy: ProxyPageClient):
        """
        Add a client to the page.

        Parameters
        ----------
        proxy : ProxyPageClient
            Client page proxy.
        """
        self.proxies.append(proxy)

    def is_available(self, models: List[Any]) -> bool:
        """
        Return whether the page is available for the current selection.

        The page is available for the selected models
        if at least one of its clients is available

        Parameters
        ----------
        models : List[Any]
            List of selected objects in the IDE.
        """
        self.active_clients = {}
        self.categories = []
        for proxy in sorted(self.proxies, key=lambda p: p.category):
            if proxy.client.is_available(models):
                self.active_clients[proxy.category] = proxy
                self.categories.append(proxy.category)
        return len(self.categories) > 0

    def on_context(self, models: List[Any]):
        """
        Declare the models the page should consider.

        Parameters
        ----------
        models : List[Any]
            List of selected objects in the IDE.
        """
        if not models:
            # deactivate the clients
            for proxy in self.active_clients.values():
                proxy.client.set_models(models)
            self.active_clients = {}
        else:
            # called between is_available and on_display,
            # seems redundant with is_available
            for proxy in self.active_clients.values():
                if not proxy.client.is_available(models):
                    if not models:
                        continue
                # assert proxy.client.is_available(models)
                proxy.client.set_models(models)

    def on_build(self):
        """Build the property page and its clients."""
        # alignment for the first line
        y = c.TOP_MARGIN
        self.cb_clients = self.add_static_combo_box(
            y, '&Tool:', style=['dropdownlist'], on_change_selection=self.on_sel_change
        )
        self.cb_clients.set_items(self.categories)
        if len(self.active_clients) > 1:
            y += c.DY
        else:
            if self.optional:
                self.cb_clients.set_visible(False)
            else:
                self.cb_clients.set_enable(False)
                y += c.DY
        for proxy in self.active_clients.values():
            proxy.client.on_build(self, y)

    def on_display(self):
        """
        Display the property page and its clients.

        Activate the last active client when possible.
        """
        assert self.cb_clients is not None  # nosec B101  # addresses linter
        selected_proxy = self.active_clients.get(self.category)
        if not selected_proxy:
            self.category = self.categories[0]
            selected_proxy = self.active_clients.get(self.category)
        self.cb_clients.set_selection(self.category)
        for proxy in self.active_clients.values():
            proxy.client.on_display()
            proxy.client.show(proxy == selected_proxy)

    def on_validate(self):
        """Validate the property page's clients."""
        for proxy in self.active_clients.values():
            proxy.client.on_validate()

    def on_close(self):
        """Perform any cleaning before the page is closed."""
        for proxy in self.active_clients.values():
            proxy.client.on_close()

    def on_layout(self):
        """Declare the contained control's constraints."""
        assert self.cb_clients is not None  # nosec B101  # addresses linter
        self.cb_clients.on_layout()
        for proxy in self.active_clients.values():
            proxy.client.on_layout()

    def on_sel_change(self, combobox: ComboBox, index: int):
        """
        Display the selected client.

        Parameters
        ----------
        combobox : ComboBox
            Control initiating the notification. Unused.

        index : int
            Index of the selected element.
        """
        new_category = self.categories[index]
        if new_category != self.category:
            self.active_clients[self.category].client.show(False)
            self.category = new_category
            self.active_clients[self.category].client.show(True)


def main():
    """Create the server property pages from the installed clients."""
    global _pages

    # get the current version and convert it to the format of srg files
    std_version = get_scade_version() * 100

    # load the page descriptions from the registered entry points
    group = 'ansys.scade.guihost'
    descriptions = sum(
        [_.load()() for _ in importlib_metadata.entry_points(group=group) if _.name == 'pages'], []
    )

    for description in descriptions:
        version = description.get('version', 0)
        expire = description.get('expire', 9999999)
        if version > std_version or expire <= std_version:
            continue
        # deprecated
        if not description.get('activate', True):
            continue
        if not description.get('active', True):
            continue
        tab = description['page']
        category = description['category']
        class_ = description['class']
        # do not display the categories when optional and only one category
        optional = description.get('optional', False)

        # get the host page for the category
        page = _pages.get(tab)
        if not page:
            page = HostPage(tab, optional)
            _pages[tab] = page
        # create the instance of the hosted page
        cls = class_()
        page.add_client(ProxyPageClient(category, cls))


# scade is a CPython module defined dynamically
try:
    main()
except BaseException as e:
    scade.tabput('LOG', f'{e}\n')  # type: ignore
    scade.tabput('LOG', f'{traceback.format_exc()}\n')  # type: ignore
else:
    scade.tabput('LOG', f'Loading GUI Host {__version__}\n')  # type: ignore
