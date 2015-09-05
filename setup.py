#!/usr/bin/env python

from setuptools import setup

setup(name='wald',
      description='Keep short text notes in a hierarchically structured document.',
      long_description=open('README.txt').read(),
      author='Claudio Jolowicz',
      author_email='cjolowicz@gmail.com',
      url='https://github.org/cjolowicz/wald',
      version='0.1',
      packages=['wald'],
      install_requires=['sqlalchemy', 'PyObjC'],
)
