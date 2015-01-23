from setuptools import setup, find_packages

setup(
  name = 'recast-api',
  version = '0.0.1',
  description = 'RECAST API',
  url = 'http://github.com/cranmer/recast-api',
  author = 'Kyle Cranmer, Lukas Heinrich',
  author_email = 'cranmer@cern.ch, lukas.heinrich@cern.ch',
  packages = find_packages(),
  intall_requires = ['requests']
)