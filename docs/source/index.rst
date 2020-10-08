|logo|

**A self-diagnosis system for vibration isolation systems in KAGRA**

|website| |release| |rtd| |license|

VISHack
=======

VISHack is a python library for system health checks of vibration isolation
systems (VIS) in KAGRA.

**Main features**

* Trigger diaggui measurements and perform system health checks with just one
  line of command.
* Powered by Python - easy integration with Guardian
* Output system health reports with highlighted alerts.

**Secondary features**

* Wraps around :code:`dtt2hdf` - extract frequency series data from diaggui
  XML files with ease.
* Trigger new measurements using existing diaggui files.

**Documentation**: https://vishack.readthedocs.io

**Repository**: https://github.com/gw-vis/vishack

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   self
   concept
   getting_started
   quick_example
   config
   command_line_utilities
   vishack_library_reference
   tutorial
   how_to_contribute
   for_developers


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |logo| image:: ../../logo.svg
    :alt: Logo
    :target: https://github.com/gw-vis/vishack

.. |website| image:: https://img.shields.io/badge/website-vishack-blue.svg
    :alt: Website
    :target: https://github.com/gw-vis/vishack

.. |release| image:: https://img.shields.io/github/v/release/gw-vis/vishack?include_prereleases
   :alt: Release
   :target: https://github.com/gw-vis/vishack/releases

.. |rtd| image:: https://readthedocs.org/projects/vishack/badge/?version=latest
   :alt: Read the Docs
   :target: https://vishack.readthedocs.io/

.. |license| image:: https://img.shields.io/github/license/gw-vis/vishack
    :alt: License
    :target: https://github.com/gw-vis/vishack/blob/master/LICENSE
