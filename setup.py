#!/usr/bin/env python

from setuptools import setup

setup(name='slacktail',
      version='0.1',
      description='Tail a file, optionaly filter, and output to Slack',
      author='Mathijs Maassen',
      author_email='m@hijs.net',
      url='https://github.com/tyz/slacktail/',
      license="MIT",
      scripts=['slacktail'],
      install_requires=['requests']
     )
