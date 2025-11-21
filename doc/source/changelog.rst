.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`2.3.1 <https://github.com/ansys/scade-guitools/releases/tag/v2.3.1>`_ - November 21, 2025
==========================================================================================

.. tab-set::


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Chore: Fix project classifiers
          - `#46 <https://github.com/ansys/scade-guitools/pull/46>`_


`2.3.0 <https://github.com/ansys/scade-guitools/releases/tag/v2.3.0>`_ - November 20, 2025
==========================================================================================

.. tab-set::


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Chore: update CHANGELOG for v2.2.0
          - `#40 <https://github.com/ansys/scade-guitools/pull/40>`_

        * - Ci: bump the actions group with 3 updates
          - `#41 <https://github.com/ansys/scade-guitools/pull/41>`_

        * - Build(deps): update sphinx-autoapi requirement from <=3.6.0 to <=3.6.1 in the dependencies group
          - `#42 <https://github.com/ansys/scade-guitools/pull/42>`_

        * - Docs: Documentation review and modifications scade-guitools
          - `#43 <https://github.com/ansys/scade-guitools/pull/43>`_


  .. tab-item:: Test

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Feat: Add an abstraction for SCADE specific commands for Python scripting
          - `#44 <https://github.com/ansys/scade-guitools/pull/44>`_


`2.2.0 <https://github.com/ansys/scade-guitools/releases/tag/v2.2.0>`_ - October 17, 2025
=========================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Feat: tech review
          - `#27 <https://github.com/ansys/scade-guitools/pull/27>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Build(deps): bump numpydoc from 1.8.0 to 1.9.0 in the dependencies group
          - `#29 <https://github.com/ansys/scade-guitools/pull/29>`_

        * - Fix: license metadata specification
          - `#30 <https://github.com/ansys/scade-guitools/pull/30>`_

        * - Build(deps): Bump build from 1.2.2.post1 to 1.3.0 in the dependencies group
          - `#33 <https://github.com/ansys/scade-guitools/pull/33>`_

        * - Docs: Update ``CONTRIBUTORS.md`` with the latest contributors
          - `#34 <https://github.com/ansys/scade-guitools/pull/34>`_

        * - Ci: Deactivate doc-deploy-pr: prevent runs conflict when merging on main
          - `#35 <https://github.com/ansys/scade-guitools/pull/35>`_

        * - Ci: Bump the actions group with 4 updates
          - `#37 <https://github.com/ansys/scade-guitools/pull/37>`_

        * - Build(deps): Bump twine from 6.1.0 to 6.2.0 in the dependencies group
          - `#38 <https://github.com/ansys/scade-guitools/pull/38>`_

        * - Fix: Allow overriding default width when adding a check button to a page.
          - `#39 <https://github.com/ansys/scade-guitools/pull/39>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - chore: update CHANGELOG for v2.1.0
          - `#24 <https://github.com/ansys/scade-guitools/pull/24>`_


  .. tab-item:: Test

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Fix: enhance robustness
          - `#31 <https://github.com/ansys/scade-guitools/pull/31>`_


`2.1.0 <https://github.com/ansys/scade-guitools/releases/tag/v2.1.0>`_ - May 22, 2025
=====================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - feat: Allow overriding default values when adding a control to a page
          - `#21 <https://github.com/ansys/scade-guitools/pull/21>`_

        * - feat: Add a mode to  FileSelector control for browsing directories
          - `#23 <https://github.com/ansys/scade-guitools/pull/23>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - fix: Do not resize check buttons
          - `#19 <https://github.com/ansys/scade-guitools/pull/19>`_


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - build(deps): Bump the dependencies group with 3 updates
          - `#8 <https://github.com/ansys/scade-guitools/pull/8>`_

        * - build(deps): Bump the dependencies group with 2 updates
          - `#10 <https://github.com/ansys/scade-guitools/pull/10>`_

        * - build(deps): Bump nbsphinx from 0.9.6 to 0.9.7 in the dependencies group across 1 directory
          - `#13 <https://github.com/ansys/scade-guitools/pull/13>`_

        * - build(deps): Update flit-core requirement from <3.11,>=3.2 to >=3.2,<3.13 in the dependencies group
          - `#16 <https://github.com/ansys/scade-guitools/pull/16>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - chore: update CHANGELOG for v2.0.0
          - `#7 <https://github.com/ansys/scade-guitools/pull/7>`_

        * - docs: Fix example
          - `#9 <https://github.com/ansys/scade-guitools/pull/9>`_

        * - chore: Enable Python 3.12 and greater
          - `#12 <https://github.com/ansys/scade-guitools/pull/12>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - ci: Fix release steps
          - `#14 <https://github.com/ansys/scade-guitools/pull/14>`_

        * - ci: Bump ansys/actions from 8 to 9 in the actions group
          - `#15 <https://github.com/ansys/scade-guitools/pull/15>`_

        * - ci: Add permissions for release action
          - `#17 <https://github.com/ansys/scade-guitools/pull/17>`_


`2.0.0 <https://github.com/ansys/scade-guitools/releases/tag/v2.0.0>`_ - 2025-01-13
===================================================================================

Added
^^^^^

- feat: Initialize the repository `#1 <https://github.com/ansys/scade-guitools/pull/1>`_
- feat: Migration to GitHub `#3 <https://github.com/ansys/scade-guitools/pull/3>`_
- feat: Add RadioBox, GroupRadioBox and StaticRadioBox controls `#6 <https://github.com/ansys/scade-guitools/pull/6>`_


Dependencies
^^^^^^^^^^^^

- build(deps): Bump the dependencies group with 2 updates `#2 <https://github.com/ansys/scade-guitools/pull/2>`_, `#4 <https://github.com/ansys/scade-guitools/pull/4>`_


Documentation
^^^^^^^^^^^^^

- docs: Review `#5 <https://github.com/ansys/scade-guitools/pull/5>`_

.. vale on
