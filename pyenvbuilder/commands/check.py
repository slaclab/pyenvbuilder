'''
Module for YAML file validation
'''
from codecs import open
import errno
from jsonschema import validate, exceptions
import yaml
import logging
from pathlib import Path


logger = logging.getLogger(__name__)
schema_dir = Path(__file__).absolute().parents[0] / 'schema.yml'


def check(**kwargs):
    '''
    Validates if proper files or directories were passed in
    '''
    # get the 'files' from the kwargs 'check' command
    get_files = (v for k, v in kwargs.items() if k == 'files')
    for file_arg in next(get_files):
        arg_path = Path(file_arg)
        # support both YAML file formats
        exts = ['.yml', '.yaml']

        if arg_path.exists():
            # validates one YAML filei
            if arg_path.is_file() and arg_path.suffix in exts:
                yaml_validator(arg_path)
            # validates a directory of YAML files
            elif arg_path.is_dir():
                for f in Path(arg_path).rglob('*'):
                    if f.suffix in exts:
                        yaml_validator(f)
        else:
            logger.error('Invalid path or file name: {}'.format(arg_path))


def add_args(cmd_parser):
    cmd_parser.add_argument('files', nargs='+')


# setting the name attribute
setattr(check, 'name', 'check')
# setting the helpp attribute
setattr(check, 'help', 'Validates and YAML file or multiple files')
# setting add_args() as attribute for check
setattr(check, 'add_args', add_args)


def yaml_loader(file_path):
    '''
    Loads an yaml file and returns its contents
    '''
    with open(file_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
            return data
        except yaml.YAMLError as err:
            logging.error('Loading YAML file error:\n {}'.format(err))


def yaml_validator(yml_file):
    '''
    Validates and YAML file against a schema
    and returns True if valid, False otherwise
    '''
    try:
        schema_file = yaml_loader(schema_dir)
        yaml_file = yaml_loader(yml_file)
        # returns None if no validation errors found
        is_valid = validate(yaml_file, schema_file)
        if is_valid is None:
            logger.info('YAML file {} is Valid'.format(yml_file))
            return True
    except OSError as e:
        if e.errno == errno.ENOENT:
            logger.error('File not found when loading yaml file')
        elif e.errno == errno.EACCES:
            logger.error('Permission denied when loading yaml file')
        else:
            logger.error('Unexpected error: {}'.format(e.errno))
    except exceptions.ValidationError as err:
        logger.error(
            'YAML Validation Error in {} for Validator: {} {}'
            .format(yml_file, err.validator, err.validator_value))
        return False
