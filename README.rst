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
* Powered by Python - easy integration with Guardian, the state-transition
  software used in KAGRA inherited from LIGO.
* Output system health reports with highlighted alerts.

**Secondary features**

* Wraps around :code:`dtt2hdf` - extract frequency series data from diaggui
  XML files with ease.
* Trigger new measurements using existing diaggui files.

**Documentation**: https://vishack.readthedocs.io

**Repository**: https://github.com/gw-vis/vishack
