import argparse

def parser():
    parser = argparse.ArgumentParser(
        description="Generate VISHack sample config")
    parser.add_argument(
        '-n', '--name', help="File name of the config",
        required=False, default='sample_config.ini')
    parser.add_argument('-o', '--overwrite',
        help='Overwrite existing file.', required=False,
        default=False)
    return parser

def main(args=None):

    import vishack.core.config

    from vishack.logger import logger

    opts = parser().parse_args(args)
    name = opts.name
    if not isinstance(opts.overwrite, bool):
        if opts.overwrite in ['True', 'true', '1', 'yes', 'Yes', 'Y', 'y']:
            overwrite = True
        else:
            overwrite = False
    else:
        overwrite = opts.overwrite
    vishack.core.config.generate_sample_config(
        name=name, overwrite=overwrite)
