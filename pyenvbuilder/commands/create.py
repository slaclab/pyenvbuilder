'''
Class for the create command
'''
import logging
from string import Template
import subprocess
import stat
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

    def run(self, **kwargs):
        # invoke conda to see if installed
        if validate_installed('conda')[0]:
            # validate files' location
            files = locate_files(**kwargs)
            for f in files:
                # check if the files are valid YAML files
                if check.yaml_validator(f)[0]:
                    data = check.yaml_loader(f)
                    if data:
                        self.conda_create(data)

    def add_args(self, cmd_parser):
        cmd_parser.add_argument(
            '--skip-tests', action='store_true', default=False)
        cmd_parser.add_argument(
            'files', nargs='+')

    def create_script(self, data):
        env_name = data['name']
        env_version = data['version']
        versioned_name = f'{env_name}_{env_version}'
        conda_packages = ' '.join(data['conda_packages'])
        pip_packages = ' '.join(data['pip_packages'] or [])

        header_template = (
            '#!/bin/bash\n')

        conda_create_template = Template(
            '$header\n'
            'conda create -n $versioned_name -c conda-forge $conda_packages\n'
            'source activate $versioned_name\n')

        pip_template = Template(
            'pip install $pip_packages\n')

        file_name = 'create_script'
        try:
            with open(file_name, 'w') as f:
                f.write(conda_create_template.substitute(
                    conda_packages=conda_packages,
                    versioned_name=versioned_name, header=header_template))
                if pip_packages.rstrip():
                    f.write(pip_template.substitute(
                        pip_packages=pip_packages))
                f.flush()
            return file_name
        except OSError as err:
            logger.error(f'Error when writing to {file_name}: {err}')
        except TypeError as err:
            logger.error(f'Error when writing {file_name}: {err}')
        except SyntaxError as err:
            logger.error(f'Syntax Error: {err}')

    def conda_create(self, data):
        '''
        here you have to check if pip-packages are not null
        ... and if tests are not null - since they are not mandatory!!!!!
        '''
        file_script = self.create_script(data)
        f = Path(file_script)
        f.chmod(f.stat().st_mode | stat.S_IEXEC)
        proc_args = Path(file_script).absolute()
        print(proc_args)

        try:
            subprocess.run(f'{proc_args}')
            # this next guy runs fine but activates the base env instead
            # left it here to try more with it
            # procc = subprocess.run(
            #    'source activate dummy_name_v0.0.0', executable='/bin/bash')
        except subprocess.CalledProcessError as err:
            logger.error(f'Some error here...calledProcessError {err}')
        except FileNotFoundError as err:
            logger.error(f'Some error here...FileNotFoundError: {err}')
        except OSError as err:
            logger.error(f'Some errors are occuring here.....{err}')
