Configuration File
==================
Each "health check" of a suspension is defined by a configuration file.
The configuration file uses the .ini format and have 7 sections: [General],
[Directory settings], [Directories], [Paths], [Coherence], [Transfer function],
and [Power spectral density]. The section names are case sensitive so it must
be exactly as stated.

Configuration file description
------------------------------

Section [General]
^^^^^^^^^^^^^^^^^
In the [General] sections, 4 parameters are taken, **Output report**,
**Report path**, **Overwrite report**, and **Alert threshold**.

- **Output report** takes a boolean value, true or false. If true,
  A report will be output to the *Report path* after the diagnosis.
- **Report path** is the path of the report. The report will be in
  reStructuredText format. Make sure to use .rst extension so it will be
  recognized in rst viewer or GitHub.
- **Overwrite report** takes a boolean value. If true, then the output report
  will replace existing files if there's file conflict.
- **Alert threshold** is a float. This defines the standard deviation threshold
  in which a measurement result is considered to be alarming. We recommend
  to set this value to 3 as it encloses 99.7% of the cases.

Section [Directory settings]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **Include subfolders** takes a boolean. If set to true, VISHack will
  walk through the specified directories and check all diaggui XML files
  including those in the subfolders, subsubfolders, etc. If set to false,
  it will only check diaggui XML files in the parent directory.

Section [Directories]
^^^^^^^^^^^^^^^^^^^^^
In this section, just list each directory, separated by newline,
with the associated diaggui XML files in it.

Section [Paths]
^^^^^^^^^^^^^^^
If there are any specific diaggui XML files that are not inside the above
directories, specify here.

Section [Coherence]
^^^^^^^^^^^^^^^^^^^
- **check** takes a boolean. If set to true, VISHack will check coherence plots
  in the diaggui files.
- **methods** takes a comma-separated list. The list of tests/evaluations to be
  perform with this "health check". Available tests are MSE, WMSE, MAE,
  WMAE, RMS, and WRMS.

Section [Transfer function]
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **check** takes a boolean. If set to true, VISHack will check transfer
  function plots in the diaggui files.
- **methods** takes a comma-separated list. The list of tests/evaluations to be
  perform with this "health check". Available tests are MSE, WMSE, MAE,
  WMAE, RMS, and WRMS.

Section [Power spectral density]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **check** takes a boolean. If set to true, VISHack will check power spectral
  density plots (actually ASDs in diaggui) in the diaggui files.
- **methods** takes a comma-separated list. The list of tests/evaluations to be
  perform with this "health check". Available tests are MSE, WMSE, MAE,
  WMAE, RMS, and WRMS.

Sample configuration file
-------------------------
VISHack has builtin command line utility function to generate a sample
configuration file. Check :ref:`Command Line Utilities` to see how to
generate a sample configuration file.

The sample configuration file looks like this:

::

  [General]
  Output report = false
  Report path = path/to/report
  Overwrite report = false
  Alert threshold = 3

  [Directory settings]
  Include subfolders = false

  [Directories]
  path/to/bs/xml/directory
  path/to/itmy/xml/dirctory

  [Paths]
  path/to/BS/BS_TM_L.xml
  path/to/any/abc.xml

  [Coherence]
  check = false
  methods = MSE,WMSE, MAE, WMAE, RMS, WRMS

  [Power spectral density]
  check = false
  methods = MSE, WMSE, MAE, WMAE, RMS, WRMS

  [Transfer function]
  check = false
  methods = MSE, WMSE, MAE, WMAE, RMS, WRMS

Modifiy the entries to suit your needs.
