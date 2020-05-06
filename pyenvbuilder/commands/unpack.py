'''
Class for the pack-command
'''
import logging
from string import Template
from pathlib import Path
import sys
from .interface import Command
from ..utils import validate_path, run_subprocess, get_destination


logger = logging.getLogger(__name__)


class Unpack(Command):
    def __init__(self):
        self.name = 'unpack'
        self.help = 'Unpacks an environment from a tarball'
        self._destination_dir = None
        self._current_dir = None

    def run(self, **kwargs):
        envs = kwargs.get('tarballs')
        self._current_dir = Path.cwd()

        # validate destination location
        dest = kwargs.get('dest')
        if dest is not None:
            dest_path, err_msg = get_destination(dest)
            if dest_path is not None:
                self._destination_dir = dest_path
            else:
                # exit the application, do not proceed if invalid destination
                sys.exit(f'Exiting application with error {err_msg}')

        for e in envs:
            if validate_path(e)[0]:
                self.unpack(e)
            else:
                logger.error(f'When unpacking could not validate path {e}')

    def add_args(self, cmd_parser):
        cmd_parser.add_argument(
            'tarballs', nargs='+')
        cmd_parser.add_argument(
            '--dest', help='Destination directory')

    def unpack(self, env):
        '''
        Unpacks an environment from a tarball

        Parameters
        ----------
        env: string
            Environment.gz name/path
        '''
        tarball_location = Path(env).absolute()
        env_name = tarball_location.name.split('.tar.gz')[0]
        env_destination = None
        if self._destination_dir is not None:
            env_destination = self._destination_dir
        else:
            env_destination = self._current_dir

        unpack_template = Template(
            'echo Unpacking the tarball for the environment $env_name\n'
            'pushd $env_destination > /dev/null\n'
            'mkdir $env_name\n'
            'tar -xzf $tarball_location -C $env_name\n'
            'source $env_name/bin/activate\n'
            'conda-unpack\n'
            'source $env_name/bin/deactivate\n'
            'popd > /dev/null\n')

        unpack_arguments = unpack_template.substitute(
            env_name=env_name, env_destination=env_destination,
            tarball_location=tarball_location)

        unpack_proc = run_subprocess(unpack_arguments)
        logger.info(f'Unpack subprocess return code: {unpack_proc.returncode}')
