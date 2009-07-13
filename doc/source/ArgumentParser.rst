ArgumentParser objects
======================

.. class:: ArgumentParser([description], [epilog], [prog], [usage], [version], [add_help], [argument_default], [parents], [prefix_chars], [conflict_handler], [formatter_class])

   Create a new :class:ArgumentParser object. Each parameter has its own more detailed description below, but in short they are:
   
   * description_ - Text to display before the argument help.
   * epilog_ - Text to display after the argument help.
   * version_ - A version number used to add a -v/--version option to the parser.
   * add_help_ - Add a -h/--help option to the parser. (default: True)
   * argument_default_ - Set the global default value for arguments. (default: None)
   * parents_ - A list of :class:ArgumentParser objects whose arguments should also be included.
   * prefix_chars_ - The set of characters that prefix optional arguments. (default: '-')
   * fromfile_prefix_chars_ - The set of characters that prefix files from which additional arguments should be read. (default: None)
   * formatter_class_ - A class for customizing the help output.
   * conflict_handler_ - Usually unnecessary, defines strategy for resolving conflicting optionals.
   * prog_ - Usually unnecessary, the name of the program (default: ``sys.argv[0]``)
   * usage_ - Usually unnecessary, the string describing the program usage (default: generated) 
   
   The following sections describe how each of these are used.


description
-----------

Most calls to the ArgumentParser constructor will use the ``description=`` keyword argument. This argument gives a brief description of what the program does and how it works. In help messages, the description is displayed between the command-line usage string and the help messages for the various arguments::

  >>> parser = argparse.ArgumentParser(description='A foo that bars')
  >>> parser.print_help()
  usage: argparse.py [-h]
  
  A foo that bars
  
  optional arguments:
    -h, --help  show this help message and exit

By default, the description will be line-wrapped so that it fits within the given space. To change this behavior, see the formatter_class_ argument.


epilog
------

Some programs like to display additional description of the program after the description of the arguments. Such text can be specified using the ``epilog=`` argument to ArgumentParser::

  >>> parser = argparse.ArgumentParser(
  ...     description='A foo that bars',
  ...     epilog="And that's how you'd foo a bar")
  >>> parser.print_help()
  usage: argparse.py [-h]
  
  A foo that bars
  
  optional arguments:
    -h, --help  show this help message and exit
  
  And that's how you'd foo a bar

As with the description_ argument, the ``epilog=`` text is by default line-wrapped, but this behavior can be adjusted with the formatter_class_ argument to ArgumentParser.


version
-------

Programs which want to display the program version at the command line can supply a version message as the ``version=`` argument to ArgumentParser. This will add a ``-v/--version`` option to the ArgumentParser that can be invoked to print the version string::

  >>> parser = argparse.ArgumentParser(prog='PROG', version='%(prog)s 3.5')
  >>> parser.print_help()
  usage: PROG [-h] [-v]
  
  optional arguments:
    -h, --help     show this help message and exit
    -v, --version  show program's version number and exit
  >>> parser.parse_args(['-v'])
  PROG 3.5

Note you can use the ``%(prog)s`` format specifier to insert the program name into the version string.


add_help
--------

By default, ArgumentParser objects add a ``-h/--help`` option which simply displays the parser's help message. For example, consider a file named ``myprogram.py`` containing the following code::

  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--foo', help='foo help')
  args = parser.parse_args()

If ``-h`` or ``--help`` is supplied is at the command-line, the ArgumentParser help will be printed::

  $ python myprogram.py --help
  usage: myprogram.py [-h] [--foo FOO]
  
  optional arguments:
    -h, --help  show this help message and exit
    --foo FOO   foo help

Occasionally, it may be useful to disable the addition of this help option. This can be achieved by passing ``False`` as the ``add_help=`` argument to ArgumentParser::

  >>> parser = argparse.ArgumentParser(prog='PROG', add_help=False)
  >>> parser.add_argument('--foo', help='foo help')
  >>> parser.print_help()
  usage: PROG [--foo FOO]
  
  optional arguments:
    --foo FOO  foo help


prefix_chars
------------

Most command-line options will use ``'-'`` as the prefix, e.g. ``-f/--foo``. Parsers that need to support additional prefix characters, e.g. for options like ``+f`` or ``/foo``, may specify them using the ``prefix_chars=`` argument to the ArgumentParser constructor::

  >>> parser = argparse.ArgumentParser(prog='PROG', prefix_chars='-+')
  >>> parser.add_argument('+f')
  >>> parser.add_argument('++bar')
  >>> parser.parse_args('+f X ++bar Y'.split())
  Namespace(bar='Y', f='X')

The ``prefix_chars=`` argument defaults to ``'-'``. Supplying a set of characters that does not include ``'-'`` will cause ``-f/--foo`` options to be disallowed.
Note that most parent parsers will specify :meth:`add_help` ``=False``. Otherwise, the ArgumentParser will see two ``-h/--help`` options (one in the parent and one in the child) and raise an error.


fromfile_prefix_chars
---------------------

Sometimes, e.g. for particularly long argument lists, it may make sense to keep the list of arguments in a file rather than typing it out at the command line.
If the ``fromfile_prefix_chars=`` argument is given to the ArgumentParser constructor, then arguments that start with any of the specified characters will be treated as files, and will be replaced by the arguments they contain. For example::

  >>> open('args.txt', 'w').write('-f\nbar')
  >>> parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
  >>> parser.add_argument('-f')
  >>> parser.parse_args(['-f', 'foo', '@args.txt'])
  Namespace(f='bar')

Arguments read from a file must be one per line (with each whole line being considered a single argument) and are treated as if they were in the same place as the original file referencing argument on the command line.
So in the example above, the expression ``['-f', 'foo', '@args.txt']`` is considered equivalent to the expression ``['-f', 'foo', '-f', 'bar']``.

The ``fromfile_prefix_chars=`` argument defaults to ``None``, meaning that arguments will never be treated as file references.


argument_default
----------------

Generally, argument defaults are specified either by passing a default to :meth:`add_argument` or by calling the :meth:`set_defaults` methods with a specific set of name-value pairs. Sometimes however, it may be useful to specify a single parser-wide default for arguments. This can be accomplished by passing the ``argument_default=`` keyword argument to ArgumentParser. For example, to globally suppress attribute creation on :meth:`parse_args` calls, we supply ``argument_default=SUPPRESS``::

  >>> parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
  >>> parser.add_argument('--foo')
  >>> parser.add_argument('bar', nargs='?')
  >>> parser.parse_args(['--foo', '1', 'BAR'])
  Namespace(bar='BAR', foo='1')
  >>> parser.parse_args([])
  Namespace()


parents
-------

Sometimes, several parsers share a common set of arguments. Rather than repeating the definitions of these arguments, you can define a single parser with all the shared arguments and then use the ``parents=`` argument to ArgumentParser to have these "inherited". The ``parents=`` argument takes a list of ArgumentParser objects, collects all the positional and optional actions from them, and adds these actions to the ArgumentParser object being constructed::

  >>> parent_parser = argparse.ArgumentParser(add_help=False)
  >>> parent_parser.add_argument('--parent', type=int)
  
  >>> foo_parser = argparse.ArgumentParser(parents=[parent_parser])
  >>> foo_parser.add_argument('foo')
  >>> foo_parser.parse_args(['--parent', '2', 'XXX'])
  Namespace(foo='XXX', parent=2)
  
  >>> bar_parser = argparse.ArgumentParser(parents=[parent_parser])
  >>> bar_parser.add_argument('--bar')
  >>> bar_parser.parse_args(['--bar', 'YYY'])
  Namespace(bar='YYY', parent=None)


formatter_class
---------------

ArgumentParser objects allow the help formatting to be customized by specifying an alternate formatting class.
Currently, there are three such classes: ``argparse.RawDescriptionHelpFormatter``, ``argparse.RawTextHelpFormatter`` and ``argparse.ArgumentDefaultsHelpFormatter``.
The first two allow more control over how textual descriptions are displayed, while the last automatically adds information about argument default values.

By default, ArgumentParser objects line-wrap the description_ and epilog_ texts in command-line help messages::

  >>> parser = argparse.ArgumentParser(
  ...     prog='PROG',
  ...     description='''this description
  ...         was indented weird
  ...             but that is okay''',
  ...     epilog='''
  ...             likewise for this epilog whose whitespace will
  ...         be cleaned up and whose words will be wrapped
  ...         across a couple lines''')
  >>> parser.print_help()
  usage: PROG [-h]
  
  this description was indented weird but that is okay
  
  optional arguments:
    -h, --help  show this help message and exit
  
  likewise for this epilog whose whitespace will be cleaned up and whose words
  will be wrapped across a couple lines

When you have description_ and epilog_ that is already correctly formatted and should not be line-wrapped, you can indicate this by passing ``argparse.RawDescriptionHelpFormatter`` as the ``formatter_class=`` argument to ArgumentParser::

  >>> parser = argparse.ArgumentParser(
  ...     prog='PROG',
  ...     formatter_class=argparse.RawDescriptionHelpFormatter,
  ...     description=textwrap.dedent('''\
  ...         Please do not mess up this text!
  ...         --------------------------------
  ...             I have indented it
  ...             exactly the way
  ...             I want it
  ...         '''))
  >>> parser.print_help()
  usage: PROG [-h]
  
  Please do not mess up this text!
  --------------------------------
      I have indented it
      exactly the way
      I want it
  
  optional arguments:
    -h, --help  show this help message and exit

If you want to maintain whitespace for all sorts of help text (including argument descriptions), you can use ``argparse.RawTextHelpFormatter``.

The other formatter class available, ``argparse.ArgumentDefaultsHelpFormatter``, will add information about the default value of each of the arguments::

  >>> parser = argparse.ArgumentParser(
  ...     prog='PROG',
  ...     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  >>> parser.add_argument('--foo', type=int, default=42, help='FOO!')
  >>> parser.add_argument('bar', nargs='*', default=[1, 2, 3], help='BAR!')
  >>> parser.print_help()
  usage: PROG [-h] [--foo FOO] [bar [bar ...]]

  positional arguments:
    bar         BAR! (default: [1, 2, 3])

  optional arguments:
    -h, --help  show this help message and exit
    --foo FOO   FOO! (default: 42)


conflict_handler
----------------

ArgumentParser objects do not allow two actions with the same option string. By default, ArgumentParser objects will raise an exception if you try to create an argument with an option string that is already in use::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('-f', '--foo', help='old foo help')
  >>> parser.add_argument('--foo', help='new foo help')
  Traceback (most recent call last):
    ..
  ArgumentError: argument --foo: conflicting option string(s): --foo

Sometimes (e.g. when using parents_) it may be useful to simply override any older arguments with the same option string. To get this behavior, the value ``'resolve'`` can be supplied to the ``conflict_handler=`` argument of ArgumentParser::

  >>> parser = argparse.ArgumentParser(prog='PROG', conflict_handler='resolve')
  >>> parser.add_argument('-f', '--foo', help='old foo help')
  >>> parser.add_argument('--foo', help='new foo help')
  >>> parser.print_help()
  usage: PROG [-h] [-f FOO] [--foo FOO]
  
  optional arguments:
    -h, --help  show this help message and exit
    -f FOO      old foo help
    --foo FOO   new foo help

Note that ArgumentParser objects only remove an action if all of its option strings are overridden. So, in the example above, the old ``-f/--foo`` action is retained as the ``-f`` action, because only the ``--foo`` option string was overridden.


prog
----

By default, ArgumentParser objects use ``sys.argv[0]`` to determine how to display the name of the program in help messages. This default is almost always what you want because it will make the help messages match what your users have typed at the command line. For example, consider a file named ``myprogram.py`` with the following code::

  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--foo', help='foo help')
  args = parser.parse_args()

The help for this program will display ``myprogram.py`` as the program name (regardless of where the program was invoked from)::

  $ python myprogram.py --help
  usage: myprogram.py [-h] [--foo FOO]
  
  optional arguments:
    -h, --help  show this help message and exit
    --foo FOO   foo help
  $ cd ..
  $ python subdir\myprogram.py --help
  usage: myprogram.py [-h] [--foo FOO]
  
  optional arguments:
    -h, --help  show this help message and exit
    --foo FOO   foo help

To change this default behavior, another value can be supplied using the ``prog=`` argument to ArgumentParser::

  >>> parser = argparse.ArgumentParser(prog='myprogram')
  >>> parser.print_help()
  usage: myprogram [-h]
  
  optional arguments:
    -h, --help  show this help message and exit

Note that the program name, whether determined from ``sys.argv[0]`` or from the ``prog=`` argument, is available to help messages using the ``%(prog)s`` format specifier.

::

  >>> parser = argparse.ArgumentParser(prog='myprogram')
  >>> parser.add_argument('--foo', help='foo of the %(prog)s program')
  >>> parser.print_help()
  usage: myprogram [-h] [--foo FOO]
  
  optional arguments:
    -h, --help  show this help message and exit
    --foo FOO   foo of the myprogram program


usage
-----

By default, ArgumentParser objects calculate the usage message from the arguments it contains::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('--foo', nargs='?', help='foo help')
  >>> parser.add_argument('bar', nargs='+', help='bar help')
  >>> parser.print_help()
  usage: PROG [-h] [--foo [FOO]] bar [bar ...]
  
  positional arguments:
    bar          bar help
  
  optional arguments:
    -h, --help   show this help message and exit
    --foo [FOO]  foo help

If the default usage message is not appropriate for your application, you can supply your own usage message using the ``usage=`` keyword argument to ArgumentParser::

  >>> parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]')
  >>> parser.add_argument('--foo', nargs='?', help='foo help')
  >>> parser.add_argument('bar', nargs='+', help='bar help')
  >>> parser.print_help()
  usage: PROG [options]
  
  positional arguments:
    bar          bar help
  
  optional arguments:
    -h, --help   show this help message and exit
    --foo [FOO]  foo help

Note you can use the ``%(prog)s`` format specifier to fill in the program name in your usage messages.


