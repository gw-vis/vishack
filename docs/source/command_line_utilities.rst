.. _Command Line Utilities::

Command Line Utilities
======================

Generate sample configuration file
----------------------------------

.. code:: bash

   $ vishack-sample-config -h
   usage: vishack-sample-config [-h] [-n NAME] [-o]

   Generate VISHack sample config

   optional arguments:
     -h, --help            show this help message and exit
     -n NAME, --name NAME  File name of the config
     -o, --overwrite       Overwrite existing file.

Example
^^^^^^^
We can generate a sample configuration file named sample_config.ini using

.. code :: bash

   vishack-sample-config -n sample_config.ini

If you would like to overwrite any existing config file that has the same name,
just pass in the :code:`-o` or :code:`--overwrite` argument:

.. code :: bash

   vishack-sample-config -n sample_config.ini -o

Perform "health check" using a configuration file
-------------------------------------------------

.. code:: bash

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

Example
^^^^^^^
To do "health checks" using a configuration file :code:`sample_config.ini`,
type

.. code:: bash

   vishack -c sample_config.ini

In k1ctr workstations, we can use the diaggui XML files to measure new results,
in this case we can pass in the :code:`-m` or :code:`--measure` argument:

.. code:: bash

   vishack -c sample_config.ini -m

This will trigger and save new measurements using the diaggui XML files
specified in the configuration file.
