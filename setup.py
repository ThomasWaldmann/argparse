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

import argparse
import distutils.core
import os
import re


def read_description():
    readme_file = open(os.path.join(os.path.dirname(__file__), 'README.txt'))
    readme_text = readme_file.read()
    readme_file.close()
    main_desc_regexp = r'^argparse\s*[\d.]*\s*\n=======+\s*\n(.*)Requirements '
    main_desc, = re.findall(main_desc_regexp, readme_text, re.DOTALL)
    avail_desc_regexp = r'Availability & Documentation\s*\n-----+\s*\n(.*)'
    avail_desc, = re.findall(avail_desc_regexp, readme_text, re.DOTALL)
    return main_desc + avail_desc

distutils.core.setup(
    name='argparse',
    version=argparse.__version__,
    author='Steven Bethard',
    author_email='steven.bethard@gmail.com',
    url='http://code.google.com/p/argparse/',
    description='Python command-line parsing library',
    long_description = read_description(),
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
