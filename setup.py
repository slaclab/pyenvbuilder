# To use a consisten encoding
from codecs import open
from os import path

from setuptools import setup, find_packages
import versioneer

CUR_DIR = path.abspath(path.dirname(__file__))

with open(path.join(CUR_DIR, 'README.md'), 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='pyenvbuilder',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    # Author details
    author='SLAC National Accelerator Laboratory',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'pyenvbuilder=pyenvbuilder.main:main',
        ]
    },

    description='Python Environment Builder',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/slaclab/pyenvbuilder',
    license='BSD',

    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ]
)
