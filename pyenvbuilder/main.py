'''
pyenvbuilder is a tool for creating and deploying python environments
'''
import argparse
import logging
from pyenvbuilder import __version__
from .commands import check


logger = logging.getLogger(__name__)

COMMANDS = {'check': check}


def launch(command, **kwargs):
    '''
    Launch pyenvbuilder with the command specified by 'command'.
    Additional parameters are passed to the command.

    Parameters
    ==========
    command   : str

    '''
    pyenvbuilder_logger = logging.getLogger('pyenvbuilder')
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)
    pyenvbuilder_logger.addHandler(handler)
    log_level = kwargs.get('log_level', 'INFO')
    pyenvbuilder_logger.setLevel(log_level)
    handler.setLevel(log_level)

    cmd = COMMANDS.get(command)
    if cmd is not None:
        cmd(**kwargs)
    else:
        commands = [k for k in COMMANDS.keys()]
        logger.info('Provide pyenvbuilder with a command: {}'.format(commands))


def parse_arguments(*args, **kwargs):
    '''
    Defines shell commands
    '''

    project_desc = "Python Environment Builder"
    parser = argparse.ArgumentParser(description=project_desc)

    subparsers = parser.add_subparsers(
        help='commands', dest='command')

    parser.add_argument(
        '--version', action='version',
        version='PyEnvBuilder {version}'.format(version=__version__),
        help="show pyenvbuilder's version number and exit")

    parser.add_argument(
        '--log_level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='configure log level')

    for cmd in COMMANDS.values():
        cmd_parser = subparsers.add_parser(cmd.name, help=cmd.help)
        cmd.add_args(cmd_parser)

    return parser.parse_args(*args, **kwargs)


def main():
    args = parse_arguments()
    kwargs = vars(args)
    launch(**kwargs)
