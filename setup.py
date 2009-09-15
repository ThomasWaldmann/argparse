# -*- coding: utf-8 -*-

# Copyright © 2006-2009 Steven J. Bethard <steven.bethard@gmail.com>.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import distutils.core
import os
import re


def read_description():
    readme_file = open(os.path.join(os.path.dirname(__file__), 'README.txt'))
    readme_text = readme_file.read()
    readme_file.close()
    main_desc_regexp = r'^argparse\s*[\d.]*\n=======+\n(.*)Requirements &'
    main_desc, = re.findall(main_desc_regexp, readme_text, re.DOTALL)
    avail_desc_regexp = r'Availability & Documentation\n-----+\n(.*)'
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
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    py_modules=['argparse'],
)
