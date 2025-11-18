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

"""
Exercises most IDE functions.

.. Note::

   The script makes sure there are no errors by calling IDE functions.
   It does not assess necessarily the results.

This script is intended to be run from SCADE Suite, with the ``Model`` project loaded.
"""

from pathlib import Path

from scade.model import suite

from ansys.scade.apitools.info import ide as is_ide, print
from ansys.scade.guitools.ide import Ide


def run(ide: Ide):
    ide.log('start')
    print('version number:', ide.version('number'))

    project = ide.get_projects()[0]
    model = ide.get_sessions()[0].model
    package = model.packages[0]
    op = package.operators[0]
    assert model.project == project
    ide.activate_project(Path(project.pathname).name)
    assert ide.get_active_project() == project
    configuration = ide.get_active_configuration(project, 'Code Generator')
    # configuration is None with default stubs
    assert not configuration or configuration.name == 'KCG'
    cwd = Path(project.pathname).parent
    ide.selection = [package]
    assert ide.selection == [package]

    # textual tabs
    tab_text = 'TEXT'
    ide.set_output_tab(tab_text)
    ide.activate_tab(tab_text)
    ide.clear_tab(tab_text)
    log_ide = (cwd / tab_text).with_suffix('.log')
    ide.output_log(tab_text, 'on', str(log_ide))
    ide.log('one')
    ide.set_output_tab('TCL')
    ide.clear_tab(tab_text)
    ide.tabput(tab_text, 'two\n')
    ide.output_log(tab_text, 'off')
    ref_ide = log_ide.with_suffix('.ref')
    assert log_ide.read_text() == ref_ide.read_text()
    # reports
    tab_report = 'REPORT'
    log_report = (cwd / tab_report).with_suffix('.log')
    ide.create_report(tab_report, ('Object', 500, 0), ('Path', 700, 0))
    ide.output_log(tab_report, 'on', str(log_report), '|')
    ide.report(op, op.get_full_path())
    ide.output_log(tab_report, 'off')
    ref_report = log_report.with_suffix('.ref')
    assert log_report.read_text() == ref_report.read_text()
    # browsers
    tab_browser = 'BROWSER'
    icon_file = (cwd / tab_browser).with_suffix('.ico')
    ide.create_browser(tab_browser, str(icon_file), False, None)
    ide.browser_report(project)
    section = 'section'
    ide.browser_report(section, project)
    ide.browser_report(package, section)
    ide.activate_browser(tab_browser)
    # windows
    ide.open_document_view(str(cwd / 'REPORT.ref'))
    path_hello = cwd / 'hello.html'
    with path_hello.open('w') as f:
        f.write('<html><head><title>Example</title></head><body>Hello world!</body></html>\n')
    ide.open_html_view(str(path_hello), use='Hello World!', delete=True)
    ide.open_html_in_browser(str(path_hello))
    # select "Clear"
    ide.open_source_code_view(str(cwd / 'TEXT.ref'), 3, 9)
    # copy selected text
    ID_EDIT_COPY = 57634  # noqa: N806  # semantic of constant  # 0xE122
    ide.command('', ID_EDIT_COPY)
    # paste it two times so that "Clear " is displayed twice
    ID_EDIT_PASTE = 57637  # noqa: N806  # semantic of constant  # 0xE125
    ide.command('', ID_EDIT_PASTE)
    ide.command('', ID_EDIT_PASTE)
    # suite
    diagram = op.diagrams[0]
    assert isinstance(diagram, suite.NetDiagram)
    ide.print(diagram, str(cwd / 'diagram.png'), 'png', 90)
    ide.print_ssl(op, str(cwd / 'o_ssl.png'), 'png', 0)

    ide.activate(op)
    ide.locate('sc:LOCATE_PATH#Model#P::O/_L1=')
    eq = model.get_object_from_path('P::O/o=')
    tuples = [
        (eq, '007f00', 'output'),
    ]
    ide.locate_ex(tuples)

    eqs = diagram.equation_sets[0]
    ide.set_style(eqs, 'Equation Set Style')

    path_decoration = cwd / 'decoration.png'
    decoration = 'decoration'
    ide.register_decoration(decoration, str(path_decoration), str(path_decoration))
    ide.set_decoration(package, decoration)
    ide.set_decoration(op, decoration)
    ide.unset_decoration(op)

    # stubs
    ide.message_box('name', 'message', 'ok', 'information')
    ide.file_open()
    ide.file_save(str(cwd / 'my file.txt'))
    ide.browse_directory()
    ide.register_terminate_callable(None)
    ide.register_load_model_callable(None)
    ide.register_unload_model_callable(None)

    ide.printer_setup('Microsoft Print to PDF')

    ide.activate_tab('TCL')
    ide.log('end')


if is_ide:
    from ansys.scade.guitools.studio import studio

    run(studio)
