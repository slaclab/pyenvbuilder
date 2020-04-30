import logging
import shutil
import subprocess
import signal
from pathlib import Path


logger = logging.getLogger(__name__)


def validate_installed(cmd):
    """
    Locates the cmd executable

    Parameters
    ----------
    cmd : str
        Command to be tested

    Returns
    -------
    tuple
        Boolean status and string status message
    """
    locate_cmd = shutil.which(cmd)
    if locate_cmd is None:
        msg = f'{cmd} not found, please install {cmd} before proceeding.'
        logger.error(msg)
        return False, msg
    else:
        return True, ''


def validate_path(file_name):
    """
    Validates if the passed-in argument is a valid path

    Parameters
    ----------
    file_name: str
        Path to be validated

    Returns
    -------
    tuple
        Boolean status and dict to identify if the path is a file or directory
    """
    f_path = Path(file_name)
    ret_arg = {'is_file': False, 'is_dir': False}

    if f_path.exists():
        if f_path.is_file():
            ret_arg['is_file'] = True
        elif f_path.is_dir():
            ret_arg['is_dir'] = True
        return True, ret_arg
    else:
        return False, ret_arg


def locate_files(files):
    """
    If one file is passed in: verifies if it is a valid yaml file
    If folder is passed in : verifies if the folder contains valid yaml files

    Parameters
    ----------
    files: list

    Returns
    -------
    list
        List of validated yaml files
    """
    file_list = []

    for f in files:
        is_valid, f_type = validate_path(f)
        # if only one file is passed in
        if is_valid and f_type['is_file']:
            if is_yaml(f):
                file_list.append(f)
            else:
                logger.error(f'{f} is not a valid .yml or .yaml file')
        # if a folder is passed in
        elif is_valid and f_type['is_dir']:
            file_list = [ff for ff in Path(f).rglob('*') if ff and is_yaml(ff)]
            if not file_list:
                logger.error(
                    f'The directory: {f} is either empty ' +
                    'or does not contain any YAML files')
        else:
            logger.error(f'Invalid path or file name: {f}')
    return file_list


def is_yaml(yml_file):
    '''
    Validates if the file is a .yml or .yaml file
    '''
    yml_path = Path(yml_file)
    extensions = ['.yml', '.yaml']
    if yml_path.suffix in extensions:
        return True
    else:
        return False


def run_subprocess(commands):
    """
    Opens a /bin/bash subproces
    This subprocess then executes the passed-in commands

    Parameters
    ----------
    commands: string
    """
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


def setup_conda():
    conda_path = shutil.which('conda')
    conda_base_path = Path(conda_path).parents[1]
    activate_script_path = conda_base_path.joinpath(
        'etc', 'profile.d', 'conda.sh')
    return activate_script_path


def get_destination(dir_path):
    '''
    Checks if it is a valid directory destination

    Parameters
    ----------
    dir_path: string
        Path of the destination directory

    Returns
    -------
    tuple
         Path of directory or None and error message
    '''
    abs_path = None
    err_msg = ''
    if dir_path is not None:
        is_valid, path_type = validate_path(dir_path)
        if is_valid:
            if path_type['is_dir']:
                abs_path = Path(dir_path).absolute()
            else:
                err_msg = f'{dir_path} is not a valid directory'
                logger.error(err_msg)
        else:
            err_msg = f'{dir_path} is not a valid path'
            logger.error(err_msg)
    return abs_path, err_msg
