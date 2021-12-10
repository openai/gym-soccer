from setuptools import setup, find_packages

setup(name='gym_soccer',
      version='0.0.1',
      packages=[*find_packages(include=('gym_soccer', "gym_soccer.*")),],
      install_requires=['gym>=0.2.3',
                        'hfo_py>=0.2']
)
