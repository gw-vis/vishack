# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- [clitools][healthcheck] Command `vishack -c path/to/config.ini -m`.
- [data][diag] Added interface to the diagnostic tool command line interface
  `diag` which is used for measuring in k1ctr workstations.
- [core][healthcheck] Added HealthCheck.dict_to_string(),
  HealthCheck.report_to_string(), and HealthCheck.alert_to_string() to
  format the report and alert to reStructuredText. And, added
  HealthCheck.print_report() method to actually write the health check
  report.
- [core][healthcheck] Added HealthCheck.get_alerts() to store alarming
  results from HealthCheck.report to HealthCheck.alert.
- [core][healthcheck] Added HealthCheck.check() method to actually compare
  measurements to references in diaggui XML files specified in the config file.
  This method will write a report HealthCheck.report in the form of dictionary.
- [data][output] Added methods for renaming in case of file confliction.
- [core][evaluate] Added functions to evaluate RMS, WRMS, MSE, WMSE, MAE, WMAE.
- [core][evaluate] Added this function library for evaluating statistical
  quantities from frequency series.
- [data][diaggui] In Diaggui class, added get_reference() and get_results
  to get the reference and results data. These can be conveniently used in
  iterations.
- [clitools][generate_sample_config] Added command line support. Now
  sample config files can be generated with the command `vishack-sample-config`
  . Options are `-n` name and `-o` overwrite.
- [core][config] Added generate_sample_config() to automatically generate
  a sample config file.
- [core][healthcheck] Added HealthCheck class. Declare with a config file.
- [data][diaggui] Added methods Diaggui.tf(), Diaggui.csd(), Diaggui.psd(), and
  Diaggui.coh(). Also added attributes Diaggui.items, Diaggui.path.
- [data][diaggui] Added Diaggui class for handling diaggui XML files.
  The class is declared with the path to the file.
- Using mypythonlibrary(https://github.com/terrencetec/mypythonlibrary) as
  a template to create this library.
- This CHANGELOG file to hopefully serve as an evolving example of a
  standardized open source project CHANGELOG.

[Unreleased]: https://github.com/gw-vis/vishack
