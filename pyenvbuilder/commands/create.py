'''
Class for the create command
'''
import logging
from string import Template
import shutil
import subprocess
import sys
import signal
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
        self._skip_tests = False
        self._conda = 'conda'

    def setup_conda(self):
        conda_path = shutil.which('conda')
        self._conda_base_path = Path(conda_path).parents[1]
        self._activate_script_path = self._conda_base_path.joinpath(
            'etc', 'profile.d', 'conda.sh'
        )

    def run(self, **kwargs):
        # invoke conda to see if installed
        if validate_installed(self._conda)[0]:
            self.setup_conda()
            self._skip_tests = kwargs.get('skip_tests')
            # validate files' location
            files = locate_files(**kwargs)
            # check if the files are valid YAML files
            if self.check_files(files):
                for f in files:
                    data = check.yaml_loader(f)
                    if data:
                        data['file_path'] = Path(f)
                        self.conda_create(data)
            else:
                # must have found an invalid YAML file
                sys.exit(f'Application exiting... yaml validation failed')
        else:
            sys.exit(
                'Application exiting with err:' +
                f'{validate_installed(self._conda)[1]}')

    def check_files(self, file_list):
        '''
        Validate all the files in the list
        Return true only if all files are valid
        '''
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

    def conda_create(self, data):
        env_name = data['name']
        env_version = data['version']
        versioned_name = f'{env_name}_{env_version}'
        conda_packages = ' '.join(data['conda_packages'])

        # optional entries
        pip_packages = ''
        if 'pip_packages' in data.keys():
            pip_packages = ' '.join(data['pip_packages'])

        versioned_path = data['file_path'].parent.joinpath(
            versioned_name).absolute()

        conda_create_template = Template(
            'conda create --yes -p $versioned_path -c' +
            'conda-forge $conda_packages conda-pack\n'
            'source $activate_script\n'
            'conda activate $versioned_path\n')

        pip_template = Template(
            'pip install $pip_packages\n')

        tests_template = Template(
            'echo \n\n'
            'echo ------ TESTING ----- \n'
            'source $activate_script\n'
            'conda activate $versioned_path\n'
            '$tests\n')

        command_args = conda_create_template.substitute(
            conda_packages=conda_packages,
            versioned_path=versioned_path,
            activate_script=self._activate_script_path)

        if pip_packages.rstrip():
            pip_args = pip_template.substitute(
                pip_packages=pip_packages)
            command_args += pip_args

        conda_proc = self.run_subprocess(command_args)
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
                    versioned_path=versioned_path, tests=t)
                test_proc = self.run_subprocess(test_args)

                report += f'TEST {t} return code: {test_proc.returncode}\n'
            logger.info(report)

    def run_subprocess(self, commands):
        '''
        Opens a /bin/bash subprocess
        That subprocess then executes the passed-in commands
        '''
        try:
            process = subprocess.Popen(
                '/bin/bash', stdin=subprocess.PIPE, encoding='utf8')

            out, err = process.communicate(commands)
            logger.debug(f'Conda create subprocess: {out}')
            logger.debug(f'Subprocess communicate: {err}')
            return process

        except subprocess.CalledProcessError:
            logger.error(
                f'Called process returned a non-zero return code')
        except subprocess.TimeoutExpiredError:
            logger.error(
                f'Subprocess, timeout expired before the process exited')
        except KeyboardInterrupt:
            process.send_signal(signal.SIGINT)
            logger.error('Received SIGINT signal, exeting...')
        except OSError as e:
            logger.error(
                f'Subprocess tryig to execute non-existing file: {e}')
        except ValueError:
            logger.error(
                f'Subprocess, invalid argument passed in')
        except subprocess.SubprocessError as e:
            logger.error(e)
        finally:
            if process:
                process.kill()
