'''
Class for the create command
'''
import logging
import subprocess

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

    def conda_create(self, data):
        env_name = data['name']
        env_version = data['version']
        versioned_name = f'{env_name}_{env_version}'
        conda_packages = ' '.join(data['conda_packages'])
        pip_packages = ' '.join(data['pip_packages'])

        conda_args = [f'conda create -n {versioned_name} -c conda-forge {conda_packages}']
        pip_args = [f'pip install {pip_packages}']
       # activate_args = ['eval "$$(conda shell.bash hook)" || :\n'
               # 'conda activate $versioned_name\n']
       # conda_avtiv = '$CONDA_PREFIX/etc/profile.d/conda.sh && conda activate {versioned_name}'
        activate_args = [f'conda activate {versioned_name}']
        deactivate_args = [f'conda deactivate']

        '''
        here you have to check if pip-packages are not null
        ... and if tests are not null!!!!!
        '''
        try:
            # create env with conda_packages
            if True: #self.run_subprocess(conda_args).returncode == 0:
                logger.info('Successfully installed conda-forge packages')
                # activate environment - conda init???
                if subprocess.run('eval "$(conda shell.bash hook)"', shell=True).returncode == 0:
                    print(f'something ----------------')
                    logger.info(f'Activated {versioned_name} environment')
                    if subprocess.run(f'conda activate {versioned_name}', shell=True).returncode == 0:
                        print('go it--------')
                    # install pip packages 
                   # if self.run_subprocess(pip_args).returncode == 0:
                    #    logger.info('Successfully installed pip-packages')
                     #   if self.run_subprocess(deactivate_args).returncode == 0:
                      #      logger.info(f'{versioned_naem} deactivated')
            else:
                logger.error("conda create Errors...")

                
            # activate the environment just created
            # install packages using pip
            
            # deactivate environment

            ''' conda create -n $name -c conda-forge $ packages'''
            ''' conda activate $name'''
            ''' pip install $ packages '''
            # create and environment with conda-forge
            # activate it
            # install pip stuff

        except (subprocess.CalledProcessError, FileNotFoundError, OSError):

            print('some error conda-create')

    def run_subprocess(self, proc_args):
        return subprocess.run(proc_args, check=True, shell=True)

