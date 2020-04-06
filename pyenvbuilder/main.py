'''
penvbuilder entry point
'''
from pyenvbuilder.commands import add_commands

def main():
    add_commands()


if "__name__" == "__main":
    main()
