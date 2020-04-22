'''
Class for the create command
'''
import logging
from string import Template
import shutil
import subprocess
from pathlib import Path


from .interface import Command
from .check import Check
from ..utils import validate_installed, locate_files


logger = logging.getLogger(__name__)
check = Check()


class Create(Command):
    def __init__(self):
        self.name = 'create'
        self.help = 'Creates an environment, given an YAML file'
        self._conda_base_path = None
        self._activate_script_path = None

    def setup_conda(self):
        conda_path = shutil.which('conda')
        self._conda_base_path = Path(conda_path).parents[1]
        self._activate_script_path = self._conda_base_path.joinpath(
            'etc', 'profile.d', 'conda.sh'
        )

    def run(self, **kwargs):
        # invoke conda to see if installed
        if validate_installed('conda')[0]:
            self.setup_conda()
            # validate files' location
            files = locate_files(**kwargs)
            for f in files:
                # check if the files are valid YAML files
                if check.yaml_validator(f)[0]:
                    data = check.yaml_loader(f)
                    if data:
                        data['file_path'] = Path(f)
                        self.conda_create(data)

    def add_args(self, cmd_parser):
        cmd_parser.add_argument(
            '--skip-tests', action='store_true', default=False)
        cmd_parser.add_argument(
            'files', nargs='+')

    def conda_create(self, data):
        env_name = data['name']
        env_version = data['version']
        versioned_name = f'{env_name}_{env_version}'
        conda_packages = ' '.join(data['conda_packages'])
        pip_packages = ' '.join(data['pip_packages'] or [])

        versioned_path = data['file_path'].parent.joinpath(
            versioned_name).absolute()

        conda_create_template = Template(
            'conda create --yes -p $versioned_path -c' +
            'conda-forge $conda_packages\n'
            'source $activate_script\n'
            'conda activate $versioned_path\n')

        pip_template = Template(
            'pip install $pip_packages\n')

        command_args = conda_create_template.substitute(
                conda_packages=conda_packages,
                versioned_path=versioned_path,
                activate_script=self._activate_script_path)
        if pip_packages.rstrip():
            pip_args = pip_template.substitute(
                pip_packages=pip_packages)
            command_args += pip_args

        conda_proc = self.run_subprocess(command_args)
        logger.info(f'Conda create subprocess return: {conda_proc.returncode}')

    def run_subprocess(self, commands):
        '''
        Opens a /bin/bash subprocess
        That subprocess then executes the passed in commands
        '''
        try:
            process = subprocess.Popen(
                '/bin/bash', stdin=subprocess.PIPE, encoding='utf8')

            out, err = process.communicate(commands)
            logger.debug(f'Conda create subprocess: {out}')
            logger.debug(f'Subprocess communicate: {err}')

            return process
        except subprocess.CalledProcessError as err:
            logger.error(f'When running coda create subprocess: {err}')
        except FileNotFoundError as err:
            logger.error(f'When running conda create subprocess: {err}')
        except OSError as err:
            logger.error(f'When running conda create subprocess: {err}')
