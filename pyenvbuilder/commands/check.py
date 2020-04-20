'''
Class for YAML file validation
'''
from codecs import open
import errno
from jsonschema import validate, exceptions
import yaml
import logging
from pathlib import Path
from .interface import Command
from ..utils import locate_files


logger = logging.getLogger(__name__)


class Check(Command):
    def __init__(self):
        self.name = 'check'
        self.help = 'Validates an YAML file or multiple files'

        self.schema_dir = Path(__file__).absolute().parents[0] / 'schema.yml'

    def run(self, **kwargs):
        '''
        Validates if proper files or directories were passed in
        '''
        files = locate_files(**kwargs)
        for f in files:
            self.yaml_validator(f)

    def add_args(self, cmd_parser):
        cmd_parser.add_argument('files', nargs='+')

    def yaml_loader(self, file_path):
        '''
        Loads an yaml file and returns its contents
        '''
        try:
            with open(file_path, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    if data is None:
                        logger.warning(f'Loading empty file: {f.name}')
                    return data
                except yaml.YAMLError as err:
                    logger.error('Loading YAML file error:\n {}'.format(err))
        except OSError as err:
            if err.errno == errno.ENOENT:
                logger.error('File not found when loading yaml file')
            elif err.errno == errno.EACCES:
                logger.error('Permission denide when loading yaml file')
            else:
                logger.error('OS error: {err}')

    def yaml_validator(self, yml_file):
        '''
        Validates and YAML file against a schema
        and returns True if valid, False otherwise
        '''
        try:
            schema_file = self.yaml_loader(self.schema_dir)
            yaml_file = self.yaml_loader(yml_file)
            if yaml_file is None:
                msg = (f'Cannot validate an empty YAML file: {yml_file}')
                logger.error(msg)
                return False, msg
            # returns None if no validation errors found
            is_valid = validate(yaml_file, schema_file)
            if is_valid is None:
                logger.info('YAML file {} is Valid'.format(yml_file))
                return True, ''
        except exceptions.ValidationError as err:
            msg = (
                'YAML Validation Error in {}:\n {}'
                .format(yml_file, err.message))
            logger.error(msg)
            return False, msg
