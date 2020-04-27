import logging
import shutil
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


def validate_path(args):
    """
    Validates if the passed-in argument is a valid path

    Parameters
    ----------
    args: str
        Path to be validated

    Returns
    -------
    tuple
        Boolean status and dict to identify if the path is a file or directory
    """
    f_path = Path(args)
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
