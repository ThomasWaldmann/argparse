# -*- coding: utf-8 -*-

# Copyright © 2006-2009 Steven J. Bethard <steven.bethard@gmail.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import textwrap
import distutils.core
import argparse

distutils.core.setup(
    name='argparse',
    version=argparse.__version__,
    author='Steven Bethard',
    author_email='steven.bethard@gmail.com',
    url='http://code.google.com/p/argparse/',
    description='Python command-line parsing library',
    long_description = textwrap.dedent("""\
        The argparse module provides an easy, declarative interface for
        creating command line tools.
        """),
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    py_modules=['argparse'],
)
