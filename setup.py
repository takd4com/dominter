#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import io

import dominter


setup(
    name='dominter',
    version=dominter.version,
    description='A simple GUI package for small asynchronous web application',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    author='Tamini Bean',
    author_email='takd4com@gmail.com',
    packages=['dominter', ],
    package_data={'dominter': ['dominter.html', 'dominter.js', ], },
    license='MIT',
    install_requires=['tornado', ],
    test_suite='test',
    url='https://github.com/takd4com/dominter',
    keywords='dom browser gui asynchronous web',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
    ],
)
