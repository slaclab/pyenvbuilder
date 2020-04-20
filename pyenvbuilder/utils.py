import logging
import subprocess
from pathlib import Path


logger = logging.getLogger(__name__)


def validate_installed(args):
    '''
    Invokes the args and returns True if successful
    '''
    try:
        if subprocess.run(args, check=True, stdout=subprocess.DEVNULL):
            return True, f''
    except subprocess.CalledProcessError as err:
        logger.error(err)
        return False, err
    except FileNotFoundError:
        msg = f'{args} not found, please install {args} before proceeding.'
        logger.error(msg)
        return False, msg


def validate_path(args):
    '''
    Validates if args is valid path
    Returns True/False and returns if is_file/is_dir
    '''
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


def locate_files(**kwargs):
    '''
    Verifies if the folder that is passed in contains yaml files
    Returns a list of yaml files
    If only one file is passed, a list of one file will be returned
    '''
    files = kwargs.get('files', [])
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
    Validate is the file is a .yml or .yaml file
    '''
    yml_path = Path(yml_file)
    extensions = ['.yml', '.yaml']
    if yml_path.suffix in extensions:
        return True
    else:
        return False
