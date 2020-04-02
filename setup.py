import versioneer
from setuptools import setup, find_packages

# To use a consisten encoding
from codecs import open
from os import path

cur_dir = path.abspath(path.dirname(__file__))

with open(path.join(cur_dir, 'README.md'), 'r', encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='pyenvbuilder',
  version=versioneer.get_version(),
  cmdclass=versioneer.get_cmdclass(),

  # Author details
  author='SLAC National Accelerator Laboratory',

  packages=find_packages(),
  description='Python Environment Builder',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/slaclab/pyenvbuilder',
  license ='BSD', 

  classifiers=[
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
  ]
)
