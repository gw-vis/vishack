import argparse

def parser():
    parser = argparse.ArgumentParser(description="Print vishack")
    parser.add_argument(
        "-n", type=int, help="just a dummy argument", required=False)
    return parser

def main(args=None):
    import vishack
    from vishack.logger import logger
    version = vishack.__version__
    logger.info('This is vishack version {}'.format(version))
