.. _argparse-vs-optparse:

argparse vs. optparse
=====================

The optparse module already comes in the Python standard library. So why would you want to use argparse instead? Here's a few of the many reasons:

* The argparse module can handle positional and optional arguments, while optparse can handle only optional arguments. (See :meth:`add_argument`.)

* The argparse module isn't dogmatic about what your command line interface should look like - options like ``-file`` or ``/file`` are supported, as are required options. Optparse refuses to support these features, preferring purity over practicality.

* The argparse module produces more informative usage messages, including command-line usage determined from your arguments, and help messages for both positional and optional arguments. The optparse module requires you to write your own usage string, and has no way to display help for positional arguments.

* The argparse module supports action that consume a variable number of command-line args, while optparse requires that the exact number of arguments (e.g. 1, 2, or 3) be known in advance.  (See :meth:`add_argument`.)

* The argparse module supports parsers that dispatch to sub-commands, while optparse requires setting ``allow_interspersed_args`` and doing the parser dispatch manually. (See :meth:`add_subparsers`.)

* The argparse module allows the ``type`` and ``action`` parameters to :meth:`add_argument` to be specified with simple callables, while optparse requires hacking class attributes like ``STORE_ACTIONS`` or ``CHECK_METHODS`` to get proper argument checking. (See :meth:`add_argument`).

The following sections discuss some of these points and a few of the other advantages of the argparse module.

Advantages of argparse
----------------------

Positional arguments
~~~~~~~~~~~~~~~~~~~~

The argparse module supports optional and positional arguments in a manner similar to the optparse module::

  >>> import argparse
  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('--foo', help='optional foo')
  >>> parser.add_argument('bar', help='positional bar')
  >>> values = parser.parse_args('--foo spam badger'.split())
  >>> values.foo
  'spam'
  >>> values.bar
  'badger'


Some of the important differences illustrated here:

* ArgumentParser objects use an :meth:`add_argument` method instead of ``add_option``. The APIs are quite similar to the optparse ones, and support the keyword arguments ``action``, ``dest``, ``nargs``, ``const``, ``default``, ``type``, ``choices``, ``help`` and ``metavar`` in much the same way that optparse does (with differences noted below).
    
* The :meth:`parse_args` method returns a single namespace object, not a ``(namespace, remaining_args)`` pair. What used to be remaining arguments with optparse are now taken care of by argparse's positional arguments.


Optional arguments
~~~~~~~~~~~~~~~~~~

The argparse module doesn't try to dictate what your command line interface should look like. You want single dashes but long option names? Sure! You want to use ``'+'`` as a flag character? Sure! You want required options? Sure!

  >>> parser = argparse.ArgumentParser(prog='PROG', prefix_chars='-+')
  >>> parser.add_argument('-foo')
  >>> parser.add_argument('+bar', required=True)
  >>> parser.parse_args('-foo 1 +bar 2'.split())
  Namespace(bar='2', foo='1')
  >>> parser.parse_args('-foo X'.split())
  usage: PROG [-h] [-foo FOO] +bar BAR
  PROG: error: argument +bar is required


Generated usage
~~~~~~~~~~~~~~~

With optparse, if you don't supply a usage string, you typically end up with ``"PROG [options]"`` displayed for usage. Since the ArgumentParser objects know both your optional and positional arguments, if you don't supply your own usage string, a reasonable one will be derived for you::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('-w', choices='123', help='w help')
  >>> parser.add_argument('-x', nargs='+', help='x help')
  >>> parser.add_argument('y', nargs='?', help='y help')
  >>> parser.add_argument('z', nargs='*', help='z help')
  >>> parser.parse_args('-x 2 3 -w 1 a b c d'.split())
  Namespace(w='1', x=['2', '3'], y='a', z=['b', 'c', 'd'])
  >>> parser.print_help()
  usage: PROG [-h] [-w {1,2,3}] [-x X [X ...]] [y] [z [z ...]]
  
  positional arguments:
    y             y help
    z             z help
  
  optional arguments:
    -h, --help    show this help message and exit
    -w {1,2,3}    w help
    -x X [X ...]  x help


More nargs options
~~~~~~~~~~~~~~~~~~

As you may have noticed in the previous section, the argparse module adds a number of useful new specifiers for the ``nargs`` keyword argument::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('-x', nargs='?', const='X')
  >>> parser.add_argument('-y', nargs='+')
  >>> parser.add_argument('z', nargs='*')
  >>> parser.parse_args('-y 0.5 -x'.split())
  Namespace(x='X', y=['0.5'], z=[])
  >>> parser.parse_args('-y 0.5 -xA 0 1 1 0'.split())
  Namespace(x='A', y=['0.5'], z=['0', '1', '1', '0'])

In particular argparse supports:

* ``N`` (an integer) meaning that ``N`` string args are allowed.
* A ``'?'``, meaning that zero or one string args are allowed.
* A ``'*'``, meaning that zero or more string args are allowed.
* A ``'+'``, meaning that one or more string args are allowed.

By default, a single argument is accepted. For everything but ``'?'`` and the default, a list of values will be produced instead of single value.


Sub-commands
~~~~~~~~~~~~

With optparse, dispatching to subparsers required disallowing interspersed args and then manually matching arg names to parsers. With the argparse module, sub-parsers are supported through the :meth:`add_subparsers` method. The :meth:`add_subparsers` method creates and returns a positional argument that exposes an ``add_parser`` method from which new named parsers can be created::

  >>> # create the base parser with a subparsers argument
  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('--bar')
  >>> subparsers = parser.add_subparsers()
  
  >>> # add a sub-command "abc"
  >>> parser_abc = subparsers.add_parser('abc')
  >>> parser_abc.add_argument('-a', action='store_true')
  >>> parser_abc.add_argument('--b', type=int)
  >>> parser_abc.add_argument('c', nargs=2)
  
  >>> # add a sub-command "xyz"
  >>> parser_xyz = subparsers.add_parser('xyz')
  >>> parser_xyz.add_argument('--x', dest='xxx')
  >>> parser_xyz.add_argument('-y', action='store_const', const=object)
  >>> parser_xyz.add_argument('z', choices='123')
  
  >>> # parse, using the subcommands
  >>> parser.parse_args('abc --b 2 AA BB'.split())
  Namespace(a=None, b=2, bar=None, c=['AA', 'BB'])
  >>> parser.parse_args('--bar B xyz -y 3'.split())
  Namespace(bar='B', xxx=None, y=<type 'object'>, z='3')
  >>> parser.parse_args('xyz --b 42'.split())
  usage: PROG xyz [-h] [--x XXX] [-y] {1,2,3}
  PROG xyz: error: no such option: --b

Note that in addition to all the usual arguments that are valid to the :class:`ArgumentParser` constructor, the ``add_parser`` method of a sub-parsers argument requires a name for the parser.  This is used to determine which parser is invoked at argument parsing time, and to print a more informative usage message.


Callable types
~~~~~~~~~~~~~~

The argparse module allows any callable that takes a single string argument as the value for the ``type`` keyword argument::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('x', type=float)
  >>> parser.add_argument('y', type=complex)
  >>> parser.add_argument('z', type=file)
  >>> parser.parse_args('0.625 4j argparse.py'.split())
  Namespace(x=0.625, y=4j, z=<open file 'argparse.py', mode 'r' at 0x...>)

For most users, you'll never need to specify a type in string form again.


Extensible actions
~~~~~~~~~~~~~~~~~~

The argparse module allows a more easily extensible means of providing new types of parsing actions. The easiest way of generating such a new action is to extend ``argparse.Action`` and override the ``__init__()`` and ``__call__()`` methods as necessary::

  >>> class FooAction(argparse.Action):
  ...     def __init__(self, foo, **kwargs):
  ...         super(FooAction, self).__init__(**kwargs)
  ...         self.foo = foo
  ...     def __call__(self, parser, namespace, value, option_string=None):
  ...         setattr(namespace, self.dest, self.foo % value)
  ... 
  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('-x', action=FooAction, foo='xfoox(%s)')
  >>> parser.add_argument('y', action=FooAction, foo='fyoyo(%s)')
  >>> parser.parse_args('42'.split())
  Namespace(x=None, y='fyoyo(42)')
  >>> parser.parse_args('42 -x 0'.split())
  Namespace(x='xfoox(0)', y='fyoyo(42)')

The ArgumentParser constructs your action object when :meth:`add_argument` is called, and passes on the arguments it received. Thus if you need more than the usual ``dest``, ``nargs``, etc., simply declare it in your ``__init__()`` method and provide a value for it in the corresponding call.


More choices
~~~~~~~~~~~~

In optparse, the ``choices`` keyword argument accepts only a list of strings. The argparse module allows ``choices`` to provide any container object, and tests the arg string values against this container after they have been type-converted::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('-x', nargs='+', choices='abc')
  >>> parser.add_argument('-y', type=int, choices=xrange(3))
  >>> parser.add_argument('z', type=float, choices=[0.5, 1.5])
  >>> parser.parse_args('-x a c -y 2 0.5'.split())
  Namespace(x=['a', 'c'], y=2, z=0.5)
  >>> parser.parse_args('1.0'.split())
  usage: PROG [-h] [-x {a,b,c} [{a,b,c} ...]] [-y {0,1,2}] {0.5,1.5}
  PROG: error: argument z: invalid choice: 1.0 (choose from 0.5, 1.5)

Note that if choices is supplied for an argument that consumes multiple arg strings, each arg string will be checked against those choices.


Sharing arguments
~~~~~~~~~~~~~~~~~

The argparse module allows you to construct simple inheritance hierarchies of parsers when it's convenient to have multiple parsers that share some of the same arguments::

  >>> foo_parser = argparse.ArgumentParser(add_help=False)
  >>> foo_parser.add_argument('--foo')
  >>> bar_parser = argparse.ArgumentParser(add_help=False)
  >>> bar_parser.add_argument('bar')
  >>> foo_bar_baz_parser = argparse.ArgumentParser(
  ...     parents=[foo_parser, bar_parser])
  >>> foo_bar_baz_parser.add_argument('--baz')
  >>> foo_bar_baz_parser.parse_args('--foo 1 XXX --baz 2'.split())
  Namespace(bar='XXX', baz='2', foo='1')

If you end up with a lot of parsers (as may happen if you make extensive use of subparsers), the ``parents`` argument can help dramatically reduce the code duplication.


Suppress anything
~~~~~~~~~~~~~~~~~

Both default values and help strings can be suppressed in argparse. Simply provide ``argparse.SUPPRESS`` to the appropriate keyword argument::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('--secret', help=argparse.SUPPRESS)
  >>> parser.add_argument('-d', default=argparse.SUPPRESS)

Note that when help for an argument is suppressed, that option will not be displayed in usage or help messages::

  >>> parser.print_help()
  usage: PROG [-h] [-d D]
  
  optional arguments:
    -h, --help  show this help message and exit
    -d D

And when a default is suppressed, the object returned by :meth:`parse_args` will only include an attribute for the argument if the argument was actually present in the arg strings::

  >>> parser.parse_args('--secret value'.split())
  Namespace(secret='value')
  >>> parser.parse_args('-d value'.split())
  Namespace(d='value', secret=None)


Upgrading optparse code
-----------------------

Originally, the argparse module had attempted to maintain compatibility with optparse. However, optparse was difficult to extend transparently, particularly with the changes required to support the new ``nargs=`` specifiers and better usage messges. When most everything in optparse had either been copy-pasted over or monkey-patched, it no longer seemed worthwhile to try to maintain the backwards compatibility.

A partial upgrade path from optparse to argparse:

* Replace all ``add_option()`` calls with :meth:`add_argument` calls.

* Replace ``options, args = parser.parse_args()`` with ``args = parser.parse_args()`` and add additional :meth:`add_argument` calls for the positional arguments.

* Replace callback actions and the ``callback_*`` keyword arguments with ``type`` or ``action`` arguments.

* Replace string names for ``type`` keyword arguments with the corresponding type objects (e.g. int, float, complex, etc).

* Replace ``Values`` with ``Namespace`` and ``OptionError/OptionValueError`` with ``ArgumentError``.

* Replace strings with implicit arguments such as ``%default`` or ``%prog`` with the standard python syntax to use dictionaries to format strings, that is to say, ``%(default)s`` and ``%(prog)s``.
