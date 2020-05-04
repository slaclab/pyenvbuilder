'''
Class for the pack-command
'''
import logging
from pathlib import Path
from string import Template
import sys
from .interface import Command
from ..utils import validate_path, run_subprocess, setup_conda, get_destination


logger = logging.getLogger(__name__)


class Pack(Command):
    def __init__(self):
        self.name = 'pack'
        self.help = 'Packs an environment into a tarball'
        self._keep_env = False
        self._activate_script_path = None
        self._destination_dir = None
        self._current_dir = None

    def run(self, **kwargs):
        self._keep_env = kwargs.get('keep_env')
        self._activate_script_path = setup_conda()
        envs = kwargs.get('environments')

        # validate destination location
        dest = kwargs.get('dest')
        if dest is not None:
            dest_path, err_msg = get_destination(dest)
            if dest_path is not None:
                self._destination_dir = dest_path
            else:
                # exit the application, do not proceed if invalid destination
                sys.exit(f'Exiting application with error: {err_msg}')

        self._current_dir = Path.cwd()
        for e in envs:
            if validate_path(e)[0]:
                self.conda_pack(e)
            else:
                logger.error(f'When packing could not validate path of {e}')

    def add_args(self, cmd_parser):
        cmd_parser.add_argument(
            '--keep-env', action='store_true', default=False,
            help='Keeps the environment created after packing it')
        cmd_parser.add_argument(
            'environments', nargs='+')
        cmd_parser.add_argument(
            '--dest', help='Destination directory')

    def conda_pack(self, env):
        '''
        Packs an environment into a tarball

        Parameters
        ----------
        env: string
            Environment name/path
        '''
        # handle the destination of the tarball
        env_path = Path(env).absolute()
        tarball_dest = None
        if self._destination_dir is not None:
            tarball_dest = self._destination_dir.joinpath(env_path.name)
        else:
            tarball_dest = self._current_dir.joinpath(env_path.name)
        # Keep the environment after packing it
        pack_keep_template = Template(
            'source $activate_script\n'
            'conda activate $env_path\n'
            'conda-pack -p $env_path -o $tarball_dest.tar.gz\n')
        # Remove the environment after it has been packed
        pack_template = Template(
            'source $activate_script\n'
            'conda activate $env_path\n'
            'conda-pack -p $env_path -o $tarball_dest.tar.gz\n'
            'conda deactivate\n'
            'conda remove -p $env_path --all --yes\n')

        command_template = (
            pack_keep_template if self._keep_env else pack_template)
        pack_arguments = command_template.substitute(
                env_path=env_path, tarball_dest=tarball_dest,
                activate_script=self._activate_script_path)

        pack_process = run_subprocess(pack_arguments)

        logger.info(f'Pack subprocess return code: {pack_process.returncode}')
