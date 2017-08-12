from setuptools import setup, find_packages

setup(
  name = 'recast-api',
  version = '0.1.0',
  description = 'RECAST API',
  url = 'http://github.com/recast-hep/recast-api',
  author = 'Kyle Cranmer, Lukas Heinrich',
  author_email = 'cranmer@cern.ch, lukas.heinrich@cern.ch',
  packages = find_packages(),
  entry_points = {
    'console_scripts': [
      'recast-createscan = recastapi.apicli:createscan'
    ]
  },
  install_requires = 
  [
   'requests',
   'click',
   'pyyaml',
   'termcolor',
   'urllib3',
   'pyopenssl',
   'ndg-httpsclient',
   'pyasn1',
   ]
)
