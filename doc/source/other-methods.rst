Other methods
=============

Partial parsing
---------------

.. method:: parse_known_args([args], [namespace])

Sometimes a script may only parse a few of the command line arguments, passing the remaining arguments on to another script or program.
In these cases, the :meth:`parse_known_args` method can be useful.
It works much like :meth:`parse_args` except that it does not produce an error when extra arguments are present.
Instead, it returns a two item tuple containing the populated namespace and the list of remaining argument strings.
::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo', action='store_true')
  >>> parser.add_argument('bar')
  >>> parser.parse_known_args(['--foo', '--badger', 'BAR', 'spam'])
  (Namespace(bar='BAR', foo=True), ['--badger', 'spam'])


Printing help
-------------

In most typical applications, :meth:`parse_args` will take care of formatting and printing any usage or error messages. However, should you want to format or print these on your own, several methods are available:

.. method:: print_usage([file]):

   Print a brief description of how the :class:`ArgumentParser` should be invoked on the command line.  If ``file`` is not present, ``sys.stderr`` is assumed.

.. method:: print_help([file]):

   Print a help message, including the program usage and information about the arguments registered with the :class:`ArgumentParser`. If ``file`` is not present, ``sys.stderr`` is assumed.
   
There are also variants of these methods that simply return a string instead of printing it:

.. method:: format_usage():

   Return a string containing a brief description of how the :class:`ArgumentParser` should be invoked on the command line.

.. method:: format_help():

   Return a string containing a help message, including the program usage and information about the arguments registered with the :class:`ArgumentParser`.
   


Parser defaults
---------------

.. method:: set_defaults(**kwargs)
   
   Most of the time, the attributes of the object returned by :meth:`parse_args` will be fully determined by inspecting the command-line args and the argument actions described in your :meth:`add_argument` calls.  However, sometimes it may be useful to add some additional attributes that are determined without any inspection of the command-line.  The :meth:`set_defaults` method allows you to do this::
   
     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('foo', type=int)
     >>> parser.set_defaults(bar=42, baz='badger')
     >>> parser.parse_args(['736'])
     Namespace(bar=42, baz='badger', foo=736)
   
   Note that parser-level defaults always override argument-level defaults. So if you set a parser-level default for a name that matches an argument, the old argument default will no longer be used::
   
     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('--foo', default='bar')
     >>> parser.set_defaults(foo='spam')
     >>> parser.parse_args([])
     Namespace(foo='spam')
   
   Parser-level defaults can be particularly useful when you're working with multiple parsers.  See the :meth:`add_subparsers` method for an example of this type.


Sub-commands
------------

.. method:: add_subparsers()

   A lot of programs split up their functionality into a number of sub-commands, for example, the ``svn`` program can invoke sub-commands like ``svn checkout``, ``svn update``, ``svn commit``, etc.  Splitting up functionality this way can be a particularly good idea when a program performs several different functions which require different kinds of command-line arguments.  ArgumentParser objects support the creation of such sub-commands with the :meth:`add_subparsers` method.  The :meth:`add_subparsers` method is normally called with no arguments and returns an special action object.  This object has a single method, ``add_parser``, which takes a command name and any ArgumentParser constructor arguments, and returns an ArgumentParser object that can be modified as usual.
   
   Some example usage::
   
     >>> # create the top-level parser
     >>> parser = argparse.ArgumentParser(prog='PROG')
     >>> parser.add_argument('--foo', action='store_true', help='foo help')
     >>> subparsers = parser.add_subparsers(help='sub-command help')
     >>>
     >>> # create the parser for the "a" command
     >>> parser_a = subparsers.add_parser('a', help='a help')
     >>> parser_a.add_argument('bar', type=int, help='bar help')
     >>>
     >>> # create the parser for the "b" command
     >>> parser_b = subparsers.add_parser('b', help='b help')
     >>> parser_b.add_argument('--baz', choices='XYZ', help='baz help')
     >>>
     >>> # parse some arg lists
     >>> parser.parse_args(['a', '12'])
     Namespace(bar=12, foo=False)
     >>> parser.parse_args(['--foo', 'b', '--baz', 'Z'])
     Namespace(baz='Z', foo=True)
   
   Note that the object returned by :meth:`parse_args` will only contain attributes for the main parser and the subparser that was selected by the command line (and not any other subparsers).  So in the example above, when the ``"a"`` command is specified, only the ``foo`` and ``bar`` attributes are present, and when the ``"b"`` command is specified, only the ``foo`` and ``baz`` attributes are present.
   
   Similarly, when a help message is requested from a subparser, only the help for that particular parser will be printed. The help message will not include parent parser or sibling parser messages. (You can however supply a help message for each subparser command by suppling the ``help=`` argument to ``add_parser`` as above.)
   
   ::
   
     >>> parser.parse_args(['--help'])
     usage: PROG [-h] [--foo] {a,b} ...
     
     positional arguments:
       {a,b}   sub-command help
     a     a help
     b     b help
     
     optional arguments:
       -h, --help  show this help message and exit
       --foo   foo help
     
     >>> parser.parse_args(['a', '--help'])
     usage: PROG a [-h] bar
     
     positional arguments:
       bar     bar help
     
     optional arguments:
       -h, --help  show this help message and exit
     
     >>> parser.parse_args(['b', '--help'])
     usage: PROG b [-h] [--baz {X,Y,Z}]
     
     optional arguments:
       -h, --help     show this help message and exit
       --baz {X,Y,Z}  baz help

   The :meth:`add_subparsers` method also supports ``title`` and ``description`` keyword arguments.  When either is present, the subparser's commands will appear in their own group in the help output.  For example::
   
     >>> parser = argparse.ArgumentParser()
     >>> subparsers = parser.add_subparsers(title='subcommands',
     ...                                    description='valid subcommands',
     ...                                    help='additional help')
     >>> subparsers.add_parser('foo')
     >>> subparsers.add_parser('bar')
     >>> parser.parse_args(['-h'])
     usage:  [-h] {foo,bar} ...
     
     optional arguments:
       -h, --help  show this help message and exit
     
     subcommands:
       valid subcommands
     
       {foo,bar}   additional help
     

   One particularly effective way of handling sub-commands is to combine the use of the :meth:`add_subparsers` method with calls to :meth:`set_defaults` so that each subparser knows which Python function it should execute.  For example::
   
     >>> # sub-command functions
     >>> def foo(args):
     ...     print args.x * args.y
     ...
     >>> def bar(args):
     ...     print '((%s))' % args.z
     ...
     >>> # create the top-level parser
     >>> parser = argparse.ArgumentParser()
     >>> subparsers = parser.add_subparsers()
     >>>
     >>> # create the parser for the "foo" command
     >>> parser_foo = subparsers.add_parser('foo')
     >>> parser_foo.add_argument('-x', type=int, default=1)
     >>> parser_foo.add_argument('y', type=float)
     >>> parser_foo.set_defaults(func=foo)
     >>>
     >>> # create the parser for the "bar" command
     >>> parser_bar = subparsers.add_parser('bar')
     >>> parser_bar.add_argument('z')
     >>> parser_bar.set_defaults(func=bar)
     >>>
     >>> # parse the args and call whatever function was selected
     >>> args = parser.parse_args('foo 1 -x 2'.split())
     >>> args.func(args)
     2.0
     >>>
     >>> # parse the args and call whatever function was selected
     >>> args = parser.parse_args('bar XYZYX'.split())
     >>> args.func(args)
     ((XYZYX))
   
   This way, you can let :meth:`parse_args` do all the work for you, and then just call the appropriate function after the argument parsing is complete. Associating functions with actions like this is typically the easiest way to handle the different actions for each of your subparsers. However, if you find it necessary to check the name of the subparser that was invoked, you can always provide a ``dest`` keyword argument to the :meth:`add_subparsers` call::
   
     >>> parser = argparse.ArgumentParser()
     >>> subparsers = parser.add_subparsers(dest='subparser_name')
     >>> subparser1 = subparsers.add_parser('1')
     >>> subparser1.add_argument('-x')
     >>> subparser2 = subparsers.add_parser('2')
     >>> subparser2.add_argument('y')
     >>> parser.parse_args(['2', 'frobble'])
     Namespace(subparser_name='2', y='frobble')


Argument groups
---------------

.. method:: add_argument_group([title], [description])

   By default, ArgumentParser objects group command-line arguments into "positional arguments" and "optional arguments" when displaying help messages. When there is a better conceptual grouping of arguments than this default one, appropriate groups can be created using the :meth:`add_argument_group` method::
   
     >>> parser = argparse.ArgumentParser(prog='PROG', add_help=False)
     >>> group = parser.add_argument_group('group')
     >>> group.add_argument('--foo', help='foo help')
     >>> group.add_argument('bar', help='bar help')
     >>> parser.print_help()
     usage: PROG [--foo FOO] bar
     
     group:
       bar    bar help
       --foo FOO  foo help
   
   The :meth:`add_argument_group` method returns an argument group object which has an :meth:`add_argument` method just like a regular ArgumentParser objects. When an argument is added to the group, the parser treats it just like a normal argument, but displays the argument in a separate group for help messages. The :meth:`add_argument_group` method accepts ``title`` and ``description`` arguments which can be used to customize this display::
   
     >>> parser = argparse.ArgumentParser(prog='PROG', add_help=False)
     >>> group1 = parser.add_argument_group('group1', 'group1 description')
     >>> group1.add_argument('foo', help='foo help')
     >>> group2 = parser.add_argument_group('group2', 'group2 description')
     >>> group2.add_argument('--bar', help='bar help')
     >>> parser.print_help()
     usage: PROG [--bar BAR] foo
     
     group1:
       group1 description
     
       foo    foo help
     
     group2:
       group2 description
     
       --bar BAR  bar help
   
   Note that any arguments not in your user defined groups will end up back in the usual "positional arguments" and "optional arguments" sections.


Mutual exclusion
----------------
   
.. method:: add_mutually_exclusive_group([required=False])

   Sometimes, you need to make sure that only one of a couple different options is specified on the command line. You can create groups of such mutually exclusive arguments using the :meth:`add_mutually_exclusive_group` method. When :func:`parse_args` is called, argparse will make sure that only one of the arguments in the mutually exclusive group was present on the command line::
   
     >>> parser = argparse.ArgumentParser(prog='PROG')
     >>> group = parser.add_mutually_exclusive_group()
     >>> group.add_argument('--foo', action='store_true')
     >>> group.add_argument('--bar', action='store_false')
     >>> parser.parse_args(['--foo'])
     Namespace(bar=True, foo=True)
     >>> parser.parse_args(['--bar'])
     Namespace(bar=False, foo=False)
     >>> parser.parse_args(['--foo', '--bar'])
     usage: PROG [-h] [--foo | --bar]
     PROG: error: argument --bar: not allowed with argument --foo
   
   The :meth:`add_mutually_exclusive_group` method also accepts a ``required`` argument, to indicate that at least one of the mutually exclusive arguments is required::
   
     >>> parser = argparse.ArgumentParser(prog='PROG')
     >>> group = parser.add_mutually_exclusive_group(required=True)
     >>> group.add_argument('--foo', action='store_true')
     >>> group.add_argument('--bar', action='store_false')
     >>> parser.parse_args([])
     usage: PROG [-h] (--foo | --bar)
     PROG: error: one of the arguments --foo --bar is required
   
   Note that currently mutually exclusive argument groups do not support the ``title`` and ``description`` arguments of :meth:`add_argument_group`. This may change in the future however, so you are *strongly* recommended to specify ``required`` as a keyword argument if you use it.


