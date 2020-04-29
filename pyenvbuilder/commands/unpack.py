'''
Class for the pack-command
'''
import logging
from string import Template
from .interface import Command
from ..utils import validate_path, run_subprocess


logger = logging.getLogger(__name__)


class Unpack(Command):
    def __init__(self):
        self.name = 'unpack'
        self.help = 'Unpacks an environment from a tarball'

    def run(self, **kwargs):
        envs = kwargs.get('tarballs')
        for e in envs:
            if validate_path(e)[0]:
                self.unpack(e)
            else:
                logger.error(f'When unpacking could not validate path {e}')

    def add_args(self, cmd_parser):
        cmd_parser.add_argument(
            'tarballs', nargs='+')

    def unpack(self, env):
        '''
        Unpacks an environment from a tarball

        Parameters
        ----------
        env: string
            Environment.gz name/path
        '''
        env = env.split('.tar.gz')[0]

        unpack_template = Template(
            'echo Unpacking the tarball for the environment $env_name\n'
            'mkdir $env_name\n'
            'tar -xzf $env_name.tar.gz -C $env_name\n'
            'source $env_name/bin/activate\n'
            'conda-unpack\n'
            'source $env_name/bin/deactivate\n')

        unpack_arguments = unpack_template.substitute(
            env_name=env)

        unpack_proc = run_subprocess(unpack_arguments)
        logger.info(f'Unpack subprocess return code: {unpack_proc.returncode}')
