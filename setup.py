# To use a consisten encoding
from codecs import open
from os import path

from setuptools import setup, find_packages
import versioneer

cur_dir = path.abspath(path.dirname(__file__))

with open(path.join(cur_dir, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(cur_dir, 'requirements.txt'), 'r', encoding='utf-8') as f:
    requirements = f.read().split()

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
    
    install_requires=requirements,
    description='Python Environment Builder',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/slaclab/pyenvbuilder',
    license='BSD',

    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ]
)
