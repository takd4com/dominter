#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='dominter',
    version='0.0.1',
    description='dominter is a simple GUI (Graphical User Interface) package for small web application.',
    author='Tamini Bean',
    author_email='takd4com@gmail.com',
    packages=['dominter', ],
    package_data={'dominter': ['dominter.html', 'dominter.js', ],},
    license='MIT',
    install_requires=['tornado', ],
    test_suite='test',
)
