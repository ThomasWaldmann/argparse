# -*- coding: utf-8 -*-

# Copyright © 2006-2009 Steven J. Bethard <steven.berthard@gmail.com>.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the 3-clause BSD
# license. No warranty expressed or implied.
# For details, see the accompanying file LICENSE.txt.

import textwrap
import distutils.core

distutils.core.setup(
    name='argparse',
    version='0.9.0',
    author='Steven Bethard',
    author_email='steven.bethard@gmail.com',
    url='http://argparse.python-hosting.com/',
    description='An optparse-inspired command-line parsing library',
    long_description = textwrap.dedent("""\
        Argparse takes the best of the optparse command-line parsing module
        and brings it new life. Argparse adds positional as well as
        optional arguments, the ability to create parsers for sub-commands,
        more informative help and usage messages, and much more. At the
        same time, it retains the ease and flexibility of use that made
        optparse so popular."""),
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    py_modules=['argparse'],
)
