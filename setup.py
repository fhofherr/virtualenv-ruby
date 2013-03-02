#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

setup(
    name='virtualenv-ruby',
    version='0.1',
    package_dir={
        '': 'src',
    },
    packages=['virtualenv_ruby'],
    entry_points={
        'console_scripts': [
            'virtualenv_ruby_install = virtualenv_ruby.main:main',
        ]
    }
)
