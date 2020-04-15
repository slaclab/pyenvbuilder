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
        # get the 'files' from the dictionary
        get_files = kwargs.get('files', [])
        for file_arg in get_files:
            arg_path = Path(file_arg)
            # support both YAML file formats
            exts = ['.yml', '.yaml']

            if arg_path.exists():
                # validates one YAML filei
                if arg_path.is_file() and arg_path.suffix in exts:
                    self.yaml_validator(arg_path)
                # validates a directory of YAML files
                elif arg_path.is_dir():
                    for f in Path(arg_path).rglob('*'):
                        if f.suffix in exts:
                            self.yaml_validator(f)
            else:
                logger.error('Invalid path or file name: {}'.format(arg_path))

    def add_args(self, cmd_parser):
        cmd_parser.add_argument('files', nargs='+')

    def yaml_loader(self, file_path):
        '''
        Loads an yaml file and returns its contents
        '''
        with open(file_path, 'r') as f:
            try:
                data = yaml.safe_load(f)
                return data
            except yaml.YAMLError as err:
                logger.error('Loading YAML file error:\n {}'.format(err))

    def yaml_validator(self, yml_file):
        '''
        Validates and YAML file against a schema
        and returns True if valid, False otherwise
        '''
        try:
            schema_file = self.yaml_loader(self.schema_dir)
            yaml_file = self.yaml_loader(yml_file)
            # returns None if no validation errors found
            is_valid = validate(yaml_file, schema_file)
            if is_valid is None:
                logger.info('YAML file {} is Valid'.format(yml_file))
                return True, ''
        except OSError as e:
            if e.errno == errno.ENOENT:
                logger.error('File not found when loading yaml file')
            elif e.errno == errno.EACCES:
                logger.error('Permission denied when loading yaml file')
            else:
                logger.error('Unexpected error: {}'.format(e.errno))
        except exceptions.ValidationError as err:
            msg = (
                'YAML Validation Error in {} for Validator: {} {}'
                .format(yml_file, err.validator, err.validator_value))
            logger.error(msg)
            return False, msg
