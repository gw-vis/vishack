Quick Example
=============
See here for a quick reference to the essential commands, functions and classes
that are needed to use VISHack conveniently. Don't forget to check out
:ref:`Tutorial` for a detailed step-by-step guide on how to configure and use
VISHack in both command line and Python interface.

Command line
------------

Generate a sample configuration file named `config.ini` for starting:

.. code-block:: bash

   vishack-sample-config --name config.ini

After modifying the arguments in `config.ini`, do measurements and checks.

.. code-block:: bash

   vishack --config path/to/config.ini --measure


Python
------
Similar procedure can also be done in Python interface:

.. code-block:: Python

   from vishack.core.config import generate_sample_config

   generate_sample_config(name='config.ini')

.. code-block:: Python

   import vishack

   hc = vishack.HealthCheck(config='path/to/config.ini')

   hc.check(new_measurement=True)
