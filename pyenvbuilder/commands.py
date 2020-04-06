'''
pyenvbuilder's commands
'''

import argparse
import sys
import pyenvbuilder

def add_commands():
    '''
    Defines shell commands
    '''

    parser = argparse.ArgumentParser(description='Python Environment Builder')

    parser.add_argument('--V', '--version', action='version',
                        version='pyenvbuilder {version}'.format(version=pyenvbuilder.__version__),
                        help='show version and exit')

    parser.parse_args()
    
    if len(sys.argv) <= 1:
        parser.print_help()
