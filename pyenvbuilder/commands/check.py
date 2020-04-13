'''
Module for YAML file validation
'''
from codecs import open
from jsonschema import validate, exceptions
import yaml
import logging
from pathlib import Path


logger = logging.getLogger(__name__)
schema_dir = Path(__file__).absolute().parents[0] / 'schema.yml'


def check(args):
    '''
    Validates if proper files or directories were passed in
    '''
    for arg in args:
        arg_path = Path(arg)
        exts = ['.yml', '.yaml']

        if arg_path.exists():
            # validates one YAML filei
            if arg_path.is_file() and arg_path.suffix in exts:
                yaml_validator(arg_path)
            # validates a directory of YAML files
            elif arg_path.is_dir():
                for f in Path(arg_path).rglob('*'):
                    if f.suffix in exts:
                        print('in dir: ', f)
                        yaml_validator(f)
        else:
            logger.error('Invalid path or file name: {}'.format(arg_path))


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


def yaml_validator(yaml_file):
    '''
    Validates and YAML file against a schema
    '''
    schema_file = yaml_loader(schema_dir)
    yaml_file = yaml_loader(yaml_file)
    try:
        # returns None if no validation errors found
        validate(yaml_file, schema_file)
    except exceptions.ValidationError as err:
        logger.error(
            'YAML Validation Error for Validator: {} {}'
            .format(err.validator, err.validator_value))
