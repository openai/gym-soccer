from setuptools import setup, find_packages

setup(name='gym_soccer',
      version='0.0.1',
      install_requires=['gym>=0.2.3',
                        'hfo_py>=0.2'],
      packages=[package for package in find_packages()
                if package.startswith('gym')],
)
