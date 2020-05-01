'''
Class for the create command
'''
import logging
from string import Template
import sys
from pathlib import Path


from .interface import Command
from .check import Check
from ..utils import (
    validate_installed, locate_files,
    run_subprocess, setup_conda, get_destination)

logger = logging.getLogger(__name__)
check = Check()


class Create(Command):
    def __init__(self):
        self.name = 'create'
        self.help = 'Creates an environment, given an YAML file'
        self._activate_script_path = None
        self._skip_tests = False
        self._conda = 'conda'
        self._destination_dir = None
        self._current_dir = None

    def run(self, **kwargs):
        # invoke conda to see if installed
        if validate_installed(self._conda):
            self._activate_script_path = setup_conda()
            self._skip_tests = kwargs.get('skip_tests')
            # validate files' location
            files = locate_files(kwargs.get('files'))

            # validate destination location
            dest = kwargs.get('dest')
            if dest is not None:
                dest_path, err_msg = get_destination(dest)
                if dest_path is not None:
                    self._destination_dir = dest_path
                else:
                    # exit if the user provided the --dest with an invalid path
                    sys.exit(f'Exiting application with error: {err_msg}')

            # check if the files are valid YAML files
            if self.check_files(files):
                for f in files:
                    data = check.yaml_loader(f)
                    if data:
                        data['file_path'] = Path(f)
                        self._current_dir = Path.cwd()
                        self.conda_create(data)
            else:
                # must have found an invalid YAML file
                sys.exit('Application exiting... yaml validation failed')
        else:
            sys.exit(
                'Application exiting with err:' +
                f'{validate_installed(self._conda)[1]}')

    def check_files(self, file_list):
        """
        Validates all the files in the list

        Parameters
        ----------
        file_list: list

        Returns
        -------
        Boolean
            Status if all files are valid
        """
        # check.yaml_validator(takes one file)
        are_valid = False
        for n in map(check.yaml_validator, file_list):
            are_valid = n[0]
        return are_valid

    def add_args(self, cmd_parser):
        cmd_parser.add_argument(
            '--skip-tests', action='store_true', default=False)
        cmd_parser.add_argument(
            'files', nargs='+')
        cmd_parser.add_argument(
            '--dest', help='Destination directory')

    def conda_create(self, data):
        env_name = data['name']
        env_version = data['version']
        versioned_name = f'{env_name}_{env_version}'
        conda_packages = ' '.join(data['conda_packages'])

        # optional entries
        pip_packages = ''
        if 'pip_packages' in data.keys():
            pip_packages = ' '.join(data['pip_packages'])

        # Handle the destination of the environment
        env_path = None
        destination_path = None
        versioned_path = self._current_dir.joinpath(
            versioned_name).absolute()
        if self._destination_dir is not None:
            destination_path = self._destination_dir.joinpath(
                versioned_name).absolute()
        if destination_path is not None:
            env_path = destination_path
        else:
            env_path = versioned_path

        conda_create_template = Template(
            'conda create --yes -p $env_path -c' +
            'conda-forge $conda_packages conda-pack\n'
            'source $activate_script\n'
            'conda activate $env_path\n')

        pip_template = Template(
            'pip install $pip_packages\n')

        tests_template = Template(
            'echo \n\n'
            'echo ------ TESTING ----- \n'
            'pushd $source_dir > /dev/null\n'
            'source $activate_script\n'
            'conda activate $env_path\n'
            '$tests\n'
            'popd > /dev/null\n')

        command_args = conda_create_template.substitute(
            conda_packages=conda_packages,
            env_path=env_path,
            activate_script=self._activate_script_path)

        if pip_packages.rstrip():
            pip_args = pip_template.substitute(
                pip_packages=pip_packages)
            command_args += pip_args

        conda_proc = run_subprocess(command_args)
        logger.info(
            f'Conda subprocess return code: {conda_proc.returncode}')

        '''
         go through all the tests and run a subprocess for each test
        '''
        # TODO find a better approach here
        if not self._skip_tests and 'tests' in data.keys():
            report = ''
            for t in data['tests']:
                test_args = tests_template.substitute(
                    activate_script=self._activate_script_path,
                    env_path=env_path, tests=t,
                    source_dir=data['file_path'].parents[0])
                test_proc = run_subprocess(test_args)

                report += f'TEST {t} return code: {test_proc.returncode}\n'
            logger.info(report)
