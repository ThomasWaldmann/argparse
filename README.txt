The argparse module makes it easy to write user friendly command line
interfaces.

The program defines what arguments it requires, and argparse will figure out
how to parse those out of sys.argv. The argparse module also automatically
generates help and usage messages and issues errors when users give the
program invalid arguments.

As of Python >= 2.7, the argparse module is maintained within the Python
standard library. For users who still need to support Python < 2.7, it is
also provided as a separate package, which tries to stay compatible with the
module in the standard library, but also supports older Python versions.

argparse is licensed under the Python license, for details see LICENSE.txt.

