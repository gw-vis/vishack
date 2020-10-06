import argparse

def parser():
    parser = argparse.ArgumentParser(
        description="VISHack suspension health check (self-diagnostic system)")
    parser.add_argument(
        '-c', '--config', type=str,
        help="The path of the .ini config file. If you don't have one, "\
            "You can generate a smaple config with vishack-sample-config",
        required=True)
    parser.add_argument('-m', '--measure',
        help='Trigger new measurements', action='store_true')
    return parser

def main(args=None):

    import vishack.core.healthcheck

    opts = parser().parse_args(args)
    config = opts.config
    measure = opts.measure
    hc = vishack.core.healthcheck.HealthCheck(config=config)
    hc.check(new_measurement=measure)
