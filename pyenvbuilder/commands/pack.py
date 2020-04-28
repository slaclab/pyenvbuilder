'''
Class for the pack-command
'''
import logging
from pathlib import Path
from string import Template
from .interface import Command
from ..utils import validate_path, run_subprocess, setup_conda


logger = logging.getLogger(__name__)


class Pack(Command):
    def __init__(self):
        self.name = 'pack'
        self.help = 'Packs an environment into a tarball'
        self._keep_env = False
        self._activate_script_path = None

    def run(self, **kwargs):
        self._keep_env = kwargs.get('keep_env')
        self._activate_script_path = setup_conda()
        envs = kwargs.get('environments')
        for e in envs:
            if validate_path(e)[0]:
                self.conda_pack(e)

    def add_args(self, cmd_parser):
        cmd_parser.add_argument(
            '--keep-env', action='store_true', default=False,
            help='Keeps the environment created after packing it')
        cmd_parser.add_argument(
            'environments', nargs='+')

    def conda_pack(self, env):
        '''
        Packs an environment into a tarball

        Parameters
        ----------
        env: string
            Environment name/path
        '''
        env_path = Path(env).absolute().parents[0] / env
        # Keep the environment after packing it
        pack_keep_template = Template(
            'source $activate_script\n'
            'conda activate $env_path\n'
            'conda-pack -p $env_path\n')
        # Remove the environment after it has been packed
        pack_template = Template(
            'source $activate_script\n'
            'conda activate $env_path\n'
            'conda-pack -p $env_path\n'
            'conda deactivate\n'
            'conda remove -p $env_path --all --yes\n')

        command_template = (
            pack_keep_template if self._keep_env else pack_template)
        pack_arguments = command_template.substitute(
                env_path=env_path,
                activate_script=self._activate_script_path)

        pack_process = run_subprocess(pack_arguments)

        logger.info(f'Pack subprocess return code: {pack_process.returncode}')
