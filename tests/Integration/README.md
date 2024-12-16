# Integration tests
This SCADE Studio Custom Extension allows testing manually the usage of the library.
It declares dialogs, property and settings pages.

## Setup
* Register the package to SCADE as detailed in
  [Install in user mode](<https://guitools.scade.docs.pyansys.com/version/dev/contributing.html#install-in-user-mode>).
* Register the test extension to SCADE: Run the PowerShell script
  [`reggitext.ps1`](reggitext.ps1), from its directory.
  A right click *Run with PowerShell* in the explorer window is easier.

  This commands copies `guitools_ut_ext.srg` to `%APPDATA%\SCADE\Customize` and updates it according to your working directory.

## Test procedure
### Initialization
* Run Ansys SCADE
* Verify the `Messages` output tab displays the following text:

  ```
  Loading integration tests for Ansys SCADE GUI Tools <version>.
  Integration tests for Ansys SCADE GUI Tools <version> loaded.
  ```

### Dialog
* Launch the command `Tools/Test GUI Tools/Dialog...` and verify the following dialog pops-up:

  ![Dialog](img/dialog.png)

## Clean
You may uninstall the package once the tests are completed:

* Unregister the package from SCADE as detailed in
  [Uninstall](<https://guitools.scade.docs.pyansys.com/version/dev/contributing.html#uninstall>).
* Unregister the test extension:

  ```cmd
  del %APPDATA%\SCADE\Customize\guitools_ut_ext.srg
  ```
