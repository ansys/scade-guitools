Getting started
===============
To use Ansys SCADE GUI Tools, you must have a valid license for Ansys SCADE.

For information on getting a licensed copy, see the
`Ansys SCADE Suite <https://www.ansys.com/products/embedded-software/ansys-scade-suite>`_
page on the Ansys website.

.. TODO: add >= Python 3.12 support upon 2026 R1 release

Requirements
------------
The ``ansys-scade-guitools`` package supports only the versions of Python delivered with
Ansys SCADE, starting from 2021 R2:

* 2021 R2 to 2023 R1: Python 3.7
* 2023 R2 and later: Python 3.10

.. _getting_started_install_user:

Install in user mode
--------------------
The following steps are for installing Ansys SCADE GUI Tools in user mode. If you want to
contribute to Ansys SCADE GUI Tools,
see :ref:`contribute_scade_guitools` for installing in developer mode.

#. Before installing Ansys SCADE GUI Tools in user mode, run this command to ensure that
   you have the latest version of `pip`_:

   .. code:: bash

      python -m pip install -U pip

#. Install Ansys SCADE GUI Tools with this command:

   .. code:: bash

       python -m pip install --user ansys-scade-guitools

#. For Ansys SCADE releases 2024 R1 and below, complete the installation with
   this command:

   .. code:: bash

      python -m ansys.scade.guitools.register

   .. Note::

      This additional step is not required when installing the package with
      Ansys SCADE Extension Manager.

.. LINKS AND REFERENCES
.. _pip: https://pypi.org/project/pip/
