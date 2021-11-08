Command Line Utilities
======================
VISHack can be used solely on a command line interface.

If you would like to use VISHack on Python interfaces, see
:ref:`VISHack Library Reference`.

Generate sample configuration file
----------------------------------

.. code-block:: bash

   $ vishack-sample-config -h
   usage: vishack-sample-config [-h] [-n NAME] [-o]

   Generate VISHack sample config

   optional arguments:
     -h, --help            show this help message and exit
     -n NAME, --name NAME  File name of the config
     -o, --overwrite       Overwrite existing file.

**Example**

We can generate a sample configuration file named sample_config.ini using

.. code-block:: bash

   vishack-sample-config -n sample_config.ini

If you would like to overwrite any existing config file that has the same name,
just pass in the :code:`-o` or :code:`--overwrite` argument:

.. code :: bash

   vishack-sample-config -n sample_config.ini -o

Perform "health check" using a configuration file
-------------------------------------------------

.. code-block:: bash

   $ vishack -h
   usage: vishack [-h] -c CONFIG [-m]

   VISHack suspension health check (self-diagnostic system)

   optional arguments:
     -h, --help            show this help message and exit
     -c CONFIG, --config CONFIG
                           The path of the .ini config file. If you don't have
                           one, You can generate a smaple config with vishack-
                           sample-config
     -m, --measure         Trigger new measurements

**Example**

To do "health checks" using a configuration file :code:`sample_config.ini`,
type

.. code-block:: bash

   vishack -c sample_config.ini

In k1ctr workstations, we can use the diaggui XML files to measure new results,
in this case we can pass in the :code:`-m` or :code:`--measure` argument:

.. code-block:: bash

   vishack -c sample_config.ini -m

This will trigger and save new measurements using the diaggui XML files
specified in the configuration file.

Read time averaged values from EPICS record
-------------------------------------------

.. code-block:: bash

   # vishack-read-time-average -h
   usage: vishack-read-time-average [-h] [-c CONFIG] [-g] [-f]

   Read time averaged values using EZCA and output to a file.

   optional arguments:
     -h, --help            show this help message and exit
     -c CONFIG, --config CONFIG
                           File name of the config
     -g, --get-config      Get a sample configuration file
     -f, --fake-ezca       Use fake ezca instead.

