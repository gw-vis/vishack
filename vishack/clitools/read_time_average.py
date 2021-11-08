"""Read time averaged values using EZCA and output to a file."""
import argparse
import configparser
import os

from ezca.ezca import Ezca
import pandas

from vishack.logger import logger
import vishack.data.ezca


def parser():
    parser = argparse.ArgumentParser(
        description="Read time averaged values using EZCA "
                    "and output to a file.")
    parser.add_argument(
        '-c', '--config', help="File name of the config", required=False,
        default=None)
    parser.add_argument(
        '-g', '--get-config',
        help='Get a sample configuration file', action='store_true')
    parser.add_argument(
        '-f', '--fake-ezca',
        help='Use fake ezca instead.', action='store_true')

    return parser


def main(args=None):
    opts = parser().parse_args(args)
    get_config = opts.get_config
    if get_config:
        sample_config()
        return
    if opts.config is None:
        logger.error("Please specify a configuration file. "
                     "You can use the -g argument to get a sample.")
        return

    # Parse config.
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform = str
    config.read(opts.config)
    output_path = config["config"]["output path"]
    ezca_prefix = config["config"]["ezca prefix"]
    duration = config["config"].getfloat("duration (s)")
    fs = config["config"].getfloat("sampling frequency (Hz)")

    fake_ezca = opts.fake_ezca
    if fake_ezca:
        from vishack.fakeezca import Ezca
    else:
        from ezca.ezca import Ezca
    ezca = Ezca(ezca_prefix)
    channels = list(config["channels"].keys())

    d_time_average = vishack.data.ezca.parallel_time_average(
        ezca=ezca, channels=channels, duration=duration, fs=fs)
    series = pandas.Series(d_time_average)
    series.to_csv(output_path, header=False)
    

def sample_config():
    """Get a sample configuration file."""
    import vishack.data.output
    
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform = str
    config["config"] = {
        "output path": "path/to/store/the/data",
        "ezca prefix": "VIS-BS",
        "duration (s)": 1,
        "sampling frequency (Hz)": 1,
    }
    config["channels"] = {
        "IP_IDAMP_L_INMON": None,
        "IP_IDAMP_T_INMON": None,
        "IP_IDAMP_Y_INMON": None,
    }
    path = "read_time_average.ini"
    if os.path.exists(path):
        path = vishack.data.output.rename(path, method="123")
    logger.info("Writing sample configuration file to {}.".format(path))
    with open(path, "w") as f:
        config.write(f)

