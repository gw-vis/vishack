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
print(srm_hc.alerts.keys())

# After getting new alerts, we can print new reports.
srm_hc.print_report(
    path='reports/another_report_with_new_threshold.rst',
    overwrite=True
)
