'''
Class for the create command
'''
import logging
from string import Template
import shutil
import subprocess
import stat
import shlex
from pathlib import Path
import os
import signal

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

    def create_script(self, data):
        env_name = data['name']
        env_version = data['version']
        versioned_name = f'{env_name}_{env_version}'
        conda_packages = ' '.join(data['conda_packages'])
        pip_packages = ' '.join(data['pip_packages'] or [])

        versioned_path = data['file_path'].parent.joinpath(versioned_name).absolute()

        header_template = (
            '#!/bin/bash\n')

        conda_create_template = Template(
           # '$header\n'
            'conda create --yes -p $versioned_path -c conda-forge $conda_packages\n'
            'source $activate_script\n'
            'conda activate $versioned_path\n')

        pip_template = Template(
            'pip install $pip_packages\n')

        pip_args = ''
        if pip_packages.rstrip():
            pip_args = pip_template.substitute(
                pip_packages=pip_packages)

        the_args = conda_create_template.substitute(
                conda_packages=conda_packages, 
                versioned_path=versioned_path, 
            #    header=header_template,
                activate_script=self._activate_script_path) + pip_args

    #    print(the_args)
      #  conda_process = subprocess.run(shlex.split(the_args), executable='/bin/bash')
       # conda_process = subprocess.run(shlex.split(the_args))
     #   command_list = the_args

       # if conda_process.returncode == 0:
       #     print('conda is done')
       # pip_process = subprocess.run(shlex.split(f'{command_list}'))#, executable='/bin/bash')
               # input=conda_process.stdout)
        conda_proc = self.run_subprocess(the_args)
       # if conda_proc.returncode == 0:
       # out, err = conda_proc.communicate(pip_args)
       # print(out)
      #  print(err)
            
        os.killpg(conda_proc.pid, signal.SIGTERM)
        print(conda_proc.returncode)
       #     print(pip_process.stdout)
        file_name = 'create_script'
        try:
            with open(file_name, 'w') as f:
                f.write(conda_create_template.substitute(
                    conda_packages=conda_packages,
                    versioned_path=versioned_path, header=header_template,
                    activate_script=self._activate_script_path
                ))
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

        try:
           # subprocess.run(f'{proc_args}')
           # subprocess.run()
        #   logger.info(proc.stdout.decode())
            print('')

            # this next guy runs fine but activates the base env instead
            # left it here to try more with it
            # procc = subprocess.run(
            #    'source activate dummy_name_v0.0.0', executable='/bin/bash')
        except subprocess.CalledProcessError as err:
            logger.error(f'Some error here...calledProcessError {err}')
        except FileNotFoundError as err:
            logger.error(f'Some error here...FileNotFoundError: {err}')
        except OSError as err:
            logger.error(f'Some errors are occurring here.....{err}')

    def run_subprocess(self, commands):
        process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE,
            encoding='utf8', shell=False)

        out, err = process.communicate(commands)
        return process


