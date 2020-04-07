'''
pyenvbuilder's commands
'''
import argparse
import logging
from pyenvbuilder import __version__


LOGGER = logging.getLogger(__name__)


def launch(log_level="INFO"):
    '''
    PyEnvBuilder's Launcher
    '''
    pyenvbuilder_logger = logging.getLogger('')
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)
    pyenvbuilder_logger.addHandler(handler)
    pyenvbuilder_logger.setLevel(log_level)
    handler.setLevel(log_level)


def parse_arguments(*args, **kwargs):
    '''
    Defines shell commands
    '''

    project_desc = "Python Environment Builder"
    parser = argparse.ArgumentParser(description=project_desc)

    parser.add_argument(
        '--version', action='version',
        version='PyEnvBuilder {version}'.format(version=__version__),
        help="show pyenvbuilder's version number and exit")

    parser.add_argument(
        '--log_level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='configure log level')

    return parser.parse_args(*args, **kwargs)


def main():
    args = parse_arguments()
    kwargs = vars(args)
    launch(**kwargs)
