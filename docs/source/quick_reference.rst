Quick Reference
===============

Generate sample config
----------------------

Command line
^^^^^^^^^^^^
.. code:: bash

   vishack-sample-config --name config.ini

Python
^^^^^^
.. code:: python

   from vishack.core.config import generate_sample_config

   generate_sample_config(name='config.ini')

Diagnosis (health check)
------------------------
Do new measurements and checks using a configuration file.

Command line
^^^^^^^^^^^^
.. code:: bash

   vishack --config path/to/config.ini --measure

Python
^^^^^^
.. code:: python

   import vishack

   hc = vishack.HealthCheck(config='path/to/config.ini')

   hc.check(new_measurement=True)
