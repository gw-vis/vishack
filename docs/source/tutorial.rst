.. _Tutorial::

Tutorial
========
Using VISHack to do suspension system diagnosis is a 3-step process and
first 2 steps are really just preparations that needed to be done once.
Step 3 is the line to trigger VISHack check and there are two ways, described
in section 3 and section 4, to achieve it manually.

.. contents::
   :depth: 2

Here, we present a step-by-step tutorial with an example on how to perform
self-diagnosis, otherwise known as "health check", on KAGRA's vibration
isolation systems (VIS).

All example files are avaliable at https://github.com/gw-vis/vishack/blob/master/examples

The example files have the following structure:

::

  examples
  ├── configs
  │   └── example_config.ini
  ├── diaggui
  │   └── SRM
  │       ├── F0
  │       │   ├── SRM_IDAMPL_DAMPL_20200929(1).xml
  │       │   └── SRM_IDAMPL_DAMPL_20200929(2).xml
  │       ├── IP
  │       │   └── SRM_IDAMPL_DAMPL_20200929.xml
  │       ├── SRM_IDAMPL_DAMPL_20200929(3).xml
  │       └── SRM_IDAMPL_DAMPL_20200929.xml
  ├── example_vishack_healthcheck.py
  └── reports
      ├── another_report.rst
      ├── another_report_with_new_threshold.rst
      └── srm_health_report.rst

0. Prerequisites
----------------
We assume you know how to use :code:`diaggui` to take and record
measurements as references. If you don't know how to use :code:`diaggui`,
but still want to perform measurements, good luck.

Basic knowledge of Python is encouraged. If you don't want to use the Python
interface, you can still use the command line interface of VISHack, or even
an MEDM or Guardian interface, if someone implemented these in the future.

Of course, we also assume that you have VISHack installed. If not,
do check out :ref:`Getting Started`.

1. Diaggui References
---------------------
The first step of the self-diagnosis procedure is to take references of
acceptable/accepted measurements. These measurements are those which defines
the vital status of the system. For example, a transfer function.
The way VISHack works, is that
it compares new measurement results to the references in the diaggui file.
To prevent excessive false alarms,
we recommend to have no less than 3 references of the same measurement,
and, the more, the better.
Of course, you can always add the measurements to the references when
you decided that it was a false alarm.

In general, a single "health check" of a suspension will associate
multiple diaggui XML files with references.
It is better to move all diaggui XML files into a centralized directory.
Subdirectories can also be used for sorting different measurement files.

We recommend to have separate directories for different suspensions. This is
because different suspensions can be checked in parallel.

In our case will use a single dummy diaggui XML file
`SRM_IDAMPL_DAMPL_20200929.xml` and duplicate it
as if they were separate independent measurements. In the file,
there are 14 references in total. 7 PSD measurements of the channel
`K1:VIS-SRM_IP_DAMP_L_IN1`, and 7 transfer function measurements from
`K1:VIS-SRM_IP_IDAMP_L_OUT` to `K1:VIS-SRM_IP_DAMP_L_IN1`.

The XML files are all populated inside the folder `diaggui/SRM`. There are
two subfolders `diaggui/SRM/IP` and `diaggui/SRM/F0`, just for demonstration.


2. VISHack Configuration file
-----------------------------
In the `config` folder, there's a config file named `example_config.ini`.
We will be using this configuration for the tutorial.

The configuration is as follows:

::

  [General]
  Output report = True
    # This will generate a report file.

  Report path = reports/srm_health_report.rst
    # This is the path of the report.
    # Use .rst extension to view it with reStructuredText compatible applications
    # like GitHub or Read the docs.

  Overwrite report = True
    # This will overwrite if there's file conflict.
    # If true, it will append something before writing.

  Alert threshold = 3
    # This alert threshold is in unit of standard deviation.
    # If any of the test results is off by this amount compare to the references,
    # it will be reported.

  [Directory settings]
  Include subfolders = True
    # This will include all diaggui files in the all subfolders, subsubfolders...
    # etc. In the directories specified below.

  [Directories]
  # Every diaggui XML files will be checked under these directories.
  diaggui/SRM/F0
  diaggui/SRM/IP

  [Paths]
  # Alternatively, we can specify individual files directly.
  # Repeated paths will not be checked twice.
  diaggui/SRM/SRM_IDAMPL_DAMPL_20200929.xml


  # Here are the type of results that we will check.
  # Use 'check = True' to enable it or else it will not check.
  # Type of tests available are mean-square-error (MSE),
  # Maximum absolute error (MAE), and root-mean-square (RMS).
  # Tests started with a 'W', such as WMSE, will whiten the data
  # with reference before evaluating.
  [Coherence]
  check = True
  methods = MSE,WMSE, MAE, WMAE, RMS, WRMS

  [Power spectral density]
  check = true
  methods = MSE, WMSE, MAE, WMAE, RMS, WRMS

  [Transfer function]
  check = True
  methods = MSE, WMSE, MAE, WMAE, RMS, WRMS

3. Using command line VISHack
-----------------------------
Note that the directories and paths specified in `config/example_config.ini`
are relative to the `example` directory. Therefore, we must run everything
under the `example` directory. If you would like to run the tests everywhere,
you must specify the full path of the diaggui XML files or the directories in
the configuration file.

To run the tests using the config, simply type

.. code:: bash

   vishack -c config/example_config.ini

This will generate a report named `srm_health_report.rst` in the `report`
directory. Feel free to open it to see how it looks like with your favorite
editor. If you view it on
`GitHub <https://github.com/gw-vis/vishack/blob/master/examples/reports/srm_health_report.rst>`_,
you will notice something special. If the **Overwrite report** argument
is set to false in the config, the UTC time will be appended to the file name
before outputting the report.

The above command will not trigger new measurements. If you would like to
measure new results, add :code`-m` to the command:

.. code:: bash

   vishack -c config/example_config.ini -m

If you type this on your local machine it will probably output shell error
because the :code:`diag` command is not installed on your local machine but
only on k1ctr workstations. Nevertheless, this will still generate the
report using the old reports.

4. Using VISHack in Python
--------------------------
An example Python script is available at `example_vishack_healthcheck.py`.

This is the script.

.. code:: python

  import vishack

  # Initial an HealthCheck instance with the config file
  srm_hc = vishack.HealthCheck(config='configs/example_config.ini')

  # Call check() method to do health check. Use new_measurement=True to trigger
  # New measurements. In this case you will have to wait until the measurements
  # finish. Only use this with k1ctr workstations.
  srm_hc.check(new_measurement=True)
  # If you don't have access to workstations, but you still want to check
  # diaggui files in hand, you can still do it:
  # Uncomment below.
  # srm_hc.check(new_measurement=False)

  # The new_measurement argument is False by default so specifying it with False
  # is actually redundant.

  # Since we have already specify to generate a report in the config file,
  # There is no need to generate it. In case we want to, we can use the
  # print_report() method
  srm_hc.print_report(path='reports/another_report.rst', overwrite=True)

  # To overwrite the alerts threshold in the config, we can manually generate
  # new alerts:
  srm_hc.get_alerts(threshold=1.9)


  # If we want to check what which files are associated with the alerts,
  # We can simply print:
  print(srm_hc.alert.keys())
  # Exercise: In your local machine, try changing the threshold to 2.0 and see
  # what happens to the alert.

  # After getting new alerts, we can print new reports.
  srm_hc.print_report(
      path='reports/another_report_with_new_threshold.rst',
      overwrite=True
  )
