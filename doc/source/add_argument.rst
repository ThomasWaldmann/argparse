The add_argument() method
=========================

.. method:: add_argument(name or flags..., [action], [nargs], [const], [default], [type], [choices], [required], [help], [metavar], [dest])

   Define how a single command line argument should be parsed. Each parameter has its own more detailed description below, but in short they are:
   
   * `name or flags`_ - Either a name or a list of option strings, e.g. ``foo`` or ``-f, --foo``
   * action_ - The basic type of action to be taken when this argument is encountered at the command-line.
   * nargs_ - The number of command-line arguments that should be consumed.
   * const_ - A constant value required by some action_ and nargs_ selections.
   * default_ - The value produced if the argument is absent from the command-line.
   * type_ - The type to which the command-line arg should be converted.
   * choices_ - A container of the allowable values for the argument.
   * required_ - Whether or not the command-line option may be omitted (optionals only).
   * help_ - A brief description of what the argument does.
   * metavar_ - A name for the argument in usage messages.
   * dest_ - The name of the attribute to be added to the object returned by :meth:`parse_args`.
   
   The following sections describe how each of these are used.

name or flags
-------------

The :meth:`add_argument` method needs to know whether you're expecting an optional argument, e.g. ``-f`` or ``--foo``, or a positional argument, e.g. a list of filenames. The first arguments passed to :meth:`add_argument` must therefore be either a series of flags, or a simple argument name. For example, an optional argument could be created like::

  >>> parser.add_argument('-f', '--foo')

while a positional argument could be created like::

  >>> parser.add_argument('bar')

When :meth:`parse_args` is called, optional arguments will be identified by the ``-`` prefix, and the remaining arguments will be assumed to be positional::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('-f', '--foo')
  >>> parser.add_argument('bar')
  >>> parser.parse_args(['BAR'])
  Namespace(bar='BAR', foo=None)
  >>> parser.parse_args(['BAR', '--foo', 'FOO'])
  Namespace(bar='BAR', foo='FOO')
  >>> parser.parse_args(['--foo', 'FOO'])
  usage: PROG [-h] [-f FOO] bar
  PROG: error: too few arguments

action
------

:class:`ArgumentParser` objects associate command-line args with actions.  These actions can do just about anything with the command-line args associated with them, though most actions simply add an attribute to the object returned by :meth:`parse_args`.  When you specify a new argument using the :meth:`add_argument` method, you can indicate how the command-line args should be handled by specifying the ``action`` keyword argument. The supported actions are:

* ``'store'`` - This just stores the argument's value. This is the default action. For example::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo')
    >>> parser.parse_args('--foo 1'.split())
    Namespace(foo='1')

* ``'store_const'`` - This stores the value specified by the const_ keyword argument. Note that the const_ keyword argument defaults to ``None``, so you'll almost always need to provide a value for it. The ``'store_const'`` action is most commonly used with optional arguments that specify some sort of flag.  For example::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', action='store_const', const=42)
    >>> parser.parse_args('--foo'.split())
    Namespace(foo=42)

* ``'store_true'`` and ``'store_false'`` - These store the values ``True`` and ``False`` respectively.  These are basically special cases of ``'store_const'``.  For example::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', action='store_true')
    >>> parser.add_argument('--bar', action='store_false')
    >>> parser.parse_args('--foo --bar'.split())
    Namespace(bar=False, foo=True)

* ``'append'`` - This stores a list, and appends each argument value to the list.  This is useful when you want to allow an option to be specified multiple times.  Example usage::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', action='append')
    >>> parser.parse_args('--foo 1 --foo 2'.split())
    Namespace(foo=['1', '2'])

* ``'append_const'`` - This stores a list, and appends the value specified by the const_ keyword argument to the list.  Note that the const_ keyword argument defaults to ``None``, so you'll almost always need to provide a value for it.  The ``'append_const'`` action is typically useful when you want multiple arguments to store constants to the same list, for example::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--str', dest='types', action='append_const', const=str)
    >>> parser.add_argument('--int', dest='types', action='append_const', const=int)
    >>> parser.parse_args('--str --int'.split())
    Namespace(types=[<type 'str'>, <type 'int'>])

You can also specify an arbitrary action by passing an object that implements the Action API.  The easiest way to do this is to extend ``argparse.Action``, supplying an appropriate ``__call__`` method.  The ``__call__`` method accepts four parameters:

* ``parser`` - The ArgumentParser object which contains this action.
* ``namespace`` - The namespace object that will be returned by :meth:`parse_args`. Most actions add an attribute to this object.
* ``values`` - The associated command-line args, with any type-conversions applied.  (Type-conversions are specified with the type_ keyword argument to :meth:`add_argument`.
* ``option_string`` - The option string that was used to invoke this action. The ``option_string`` argument is optional, and will be absent if the action is associated with a positional argument.

So for example::

  >>> class FooAction(argparse.Action):
  ...     def __call__(self, parser, namespace, values, option_string=None):
  ...     print '%r %r %r' % (namespace, values, option_string)
  ...     setattr(namespace, self.dest, values)
  ...     
  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo', action=FooAction)
  >>> parser.add_argument('bar', action=FooAction)
  >>> args = parser.parse_args('1 --foo 2'.split())
  Namespace(bar=None, foo=None) '1' None
  Namespace(bar='1', foo=None) '2' '--foo'
  >>> args
  Namespace(bar='1', foo='2')


nargs
-----

ArgumentParser objects usually associate a single command-line argument with a single action to be taken.  In the situations where you'd like to associate a different number of command-line arguments with a single action, you can use the ``nargs`` keyword argument to :meth:`add_argument`. The supported values are:

* N (an integer). N args from the command-line will be gathered together into a list.  For example::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', nargs=2)
    >>> parser.add_argument('bar', nargs=1)
    >>> parser.parse_args('c --foo a b'.split())
    Namespace(bar=['c'], foo=['a', 'b'])

  Note that ``nargs=1`` produces a list of one item.  This is different from the default, in which the item is produced by itself.

* ``'?'``. One arg will be consumed from the command-line if possible, and produced as a single item.  If no command-line arg is present, the value from default_ will be produced.  Note that for optional arguments, there is an additional case - the option string is present but not followed by a command-line arg.  In this case the value from const_ will be produced.  Some examples to illustrate this::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', nargs='?', const='c', default='d')
    >>> parser.add_argument('bar', nargs='?', default='d')
    >>> parser.parse_args('XX --foo YY'.split())
    Namespace(bar='XX', foo='YY')
    >>> parser.parse_args('XX --foo'.split())
    Namespace(bar='XX', foo='c')
    >>> parser.parse_args(''.split())
    Namespace(bar='d', foo='d')

  One of the more common uses of ``nargs='?'`` is to allow optional input and output files::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    >>> parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    >>> parser.parse_args(['input.txt', 'output.txt'])
    Namespace(infile=<open file 'input.txt', mode 'r' at 0x...>, outfile=<open file 'output.txt', mode 'w' at 0x...>)
    >>> parser.parse_args([])
    Namespace(infile=<open file '<stdin>', mode 'r' at 0x...>, outfile=<open file '<stdout>', mode 'w' at 0x...>)

* ``'*'``. All command-line args present are gathered into a list. Note that it generally doesn't make much sense to have more than one positional argument with ``nargs='*'``, but multiple optional arguments with ``nargs='*'`` is possible.  For example::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', nargs='*')
    >>> parser.add_argument('--bar', nargs='*')
    >>> parser.add_argument('baz', nargs='*')
    >>> parser.parse_args('a b --foo x y --bar 1 2'.split())
    Namespace(bar=['1', '2'], baz=['a', 'b'], foo=['x', 'y'])

* ``'+'``. Just like ``'*'``, all command-line args present are gathered into a list.  Additionally, an error message will be generated if there wasn't at least one command-line arg present.  For example::

    >>> parser = argparse.ArgumentParser(prog='PROG')
    >>> parser.add_argument('foo', nargs='+')
    >>> parser.parse_args('a b'.split())
    Namespace(foo=['a', 'b'])
    >>> parser.parse_args(''.split())
    usage: PROG [-h] foo [foo ...]
    PROG: error: too few arguments

If the ``nargs`` keyword argument is not provided, the number of args consumed is determined by the action_. Generally this means a single command-line arg will be consumed and a single item (not a list) will be produced.


const
-----

The ``const`` argument of :meth:`add_argument` is used to hold constant values that are not read from the command line but are required for the various ArgumentParser actions.  The two most common uses of it are:

* When :meth:`add_argument` is called with ``action='store_const'`` or ``action='append_const'``.  These actions add the ``const`` value to one of the attributes of the object returned by :meth:`parse_args`.  See the action_ description for examples.

* When :meth:`add_argument` is called with option strings (like ``-f`` or ``--foo``) and ``nargs='?'``. This creates an optional argument that can be followed by zero or one command-line args.  When parsing the command-line, if the option string is encountered with no command-line arg following it, the value of ``const`` will be assumed instead. See the nargs_ description for examples.

The ``const`` keyword argument defaults to ``None``.


default
-------

All optional arguments and some positional arguments may be omitted at the command-line.  The ``default`` keyword argument of :meth:`add_argument`, whose value defaults to ``None``, specifies what value should be used if the command-line arg is not present.  For optional arguments, the ``default`` value is used when the option string was not present at the command line::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo', default=42)
  >>> parser.parse_args('--foo 2'.split())
  Namespace(foo='2')
  >>> parser.parse_args(''.split())
  Namespace(foo=42)

For positional arguments with nargs_ ``='?'`` or ``'*'``, the ``default`` value is used when no command-line arg was present::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('foo', nargs='?', default=42)
  >>> parser.parse_args('a'.split())
  Namespace(foo='a')
  >>> parser.parse_args(''.split())
  Namespace(foo=42)


If you don't want to see an attribute when an option was not present at the command line, you can supply ``default=argparse.SUPPRESS``::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo', default=argparse.SUPPRESS)
  >>> parser.parse_args([])
  Namespace()
  >>> parser.parse_args(['--foo', '1'])
  Namespace(foo='1')


type
----

By default, ArgumentParser objects read command-line args in as simple strings. However, quite often the command-line string should instead be interpreted as another type, e.g. ``float``, ``int`` or ``file``. The ``type`` keyword argument of :meth:`add_argument` allows any necessary type-checking and type-conversions to be performed.  Many common builtin types can be used directly as the value of the ``type`` argument::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('foo', type=int)
  >>> parser.add_argument('bar', type=file)
  >>> parser.parse_args('2 temp.txt'.split())
  Namespace(bar=<open file 'temp.txt', mode 'r' at 0x...>, foo=2)

To ease the use of various types of files, the argparse module provides the factory FileType which takes the ``mode=`` and ``bufsize=`` arguments of the ``file`` object. For example, ``FileType('w')`` can be used to create a writable file::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('bar', type=argparse.FileType('w'))
  >>> parser.parse_args(['out.txt'])
  Namespace(bar=<open file 'out.txt', mode 'w' at 0x...>)

If you need to do some special type-checking or type-conversions, you can provide your own types by passing to ``type=`` a callable that takes a single string argument and returns the type-converted value::

  >>> def perfect_square(string):
  ...     value = int(string)
  ...     sqrt = math.sqrt(value)
  ...     if sqrt != int(sqrt):
  ...     raise TypeError()
  ...     return value
  ...    
  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('foo', type=perfect_square)
  >>> parser.parse_args('9'.split())
  Namespace(foo=9)
  >>> parser.parse_args('7'.split())
  usage: PROG [-h] foo
  PROG: error: argument foo: invalid perfect_square value: '7'

Note that if your type-checking function is just checking for a particular set of values, it may be more convenient to use the choices_ keyword argument::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('foo', type=int, choices=xrange(5, 10))
  >>> parser.parse_args('7'.split())
  Namespace(foo=7)
  >>> parser.parse_args('11'.split())
  usage: PROG [-h] {5,6,7,8,9}
  PROG: error: argument foo: invalid choice: 11 (choose from 5, 6, 7, 8, 9)

See the choices_ section for more details.


choices
-------

Some command-line args should be selected from a restricted set of values. ArgumentParser objects can be told about such sets of values by passing a container object as the ``choices`` keyword argument to :meth:`add_argument`. When the command-line is parsed with :meth:`parse_args`, arg values will be checked, and an error message will be displayed if the arg was not one of the acceptable values::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('foo', choices='abc')
  >>> parser.parse_args('c'.split())
  Namespace(foo='c')
  >>> parser.parse_args('X'.split())
  usage: PROG [-h] {a,b,c}
  PROG: error: argument foo: invalid choice: 'X' (choose from 'a', 'b', 'c')

Note that inclusion in the ``choices`` container is checked after any type_ conversions have been performed, so the type of the objects in the ``choices`` container should match the type_ specified::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('foo', type=complex, choices=[1, 1j])
  >>> parser.parse_args('1j'.split())
  Namespace(foo=1j)
  >>> parser.parse_args('-- -4'.split())
  usage: PROG [-h] {1,1j}
  PROG: error: argument foo: invalid choice: (-4+0j) (choose from 1, 1j)

Any object that supports the ``in`` operator can be passed as the ``choices`` value, so ``dict`` objects, ``set`` objects, custom containers, etc. are all supported.


required
--------

In general, the argparse module assumes that flags like ``-f`` and ``--bar`` indicate *optional* arguments, which can always be omitted at the command-line. To change this behavior, i.e. to make an option *required*, the value ``True`` should be specified for the ``required=`` keyword argument to :meth:`add_argument`::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo', required=True)
  >>> parser.parse_args(['--foo', 'BAR'])
  Namespace(foo='BAR')
  >>> parser.parse_args([])
  usage: argparse.py [-h] [--foo FOO]
  argparse.py: error: option --foo is required

As the example shows, if an option is marked as ``required``, :meth:`parse_args` will report an error if that option is not present at the command line.

**Warning:** Required options are generally considered bad form - normal users expect *options* to be *optional*. You should avoid the use of required options whenever possible.


help
----

A great command-line interface isn't worth anything if your users can't figure out which option does what.  So for the end-users, ``help`` is probably the most important argument to include in your :meth:`add_argument` calls.  The ``help`` value should be a string containing a brief description of what the argument specifies.  When a user requests help (usually by using ``-h`` or ``--help`` at the command-line), these ``help`` descriptions will be displayed with each argument::

  >>> parser = argparse.ArgumentParser(prog='frobble')
  >>> parser.add_argument('--foo', action='store_true',
  ...         help='foo the bars before frobbling')
  >>> parser.add_argument('bar', nargs='+',
  ...         help='one of the bars to be frobbled')
  >>> parser.parse_args('-h'.split())
  usage: frobble [-h] [--foo] bar [bar ...]
  
  positional arguments:
    bar     one of the bars to be frobbled
  
  optional arguments:
    -h, --help  show this help message and exit
    --foo   foo the bars before frobbling

The ``help`` strings can include various format specifiers to avoid repetition of things like the program name or the argument default_.  The available specifiers include the program name, ``%(prog)s`` and most keyword arguments to :meth:`add_argument`, e.g. ``%(default)s``, ``%(type)s``, etc.::

  >>> parser = argparse.ArgumentParser(prog='frobble')
  >>> parser.add_argument('bar', nargs='?', type=int, default=42,
  ...         help='the bar to %(prog)s (default: %(default)s)')
  >>> parser.print_help()
  usage: frobble [-h] [bar]
  
  positional arguments:
    bar     the bar to frobble (default: 42)
  
  optional arguments:
    -h, --help  show this help message and exit


metavar
-------

When ArgumentParser objects generate help messages, they need some way to refer to each expected argument. By default, ArgumentParser objects use the dest_ value as the "name" of each object.  By default, for positional argument actions, the dest_ value is used directly, and for optional argument actions, the dest_ value is uppercased.  So if we have a single positional argument with ``dest='bar'``, that argument will be referred to as ``bar``.  And if we have a single optional argument ``--foo`` that should be followed by a single command-line arg, that arg will be referred to as ``FOO``.  You can see this behavior in the example below::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo')
  >>> parser.add_argument('bar')
  >>> parser.parse_args('X --foo Y'.split())
  Namespace(bar='X', foo='Y')
  >>> parser.print_help()
  usage:  [-h] [--foo FOO] bar
  
  positional arguments:
    bar
  
  optional arguments:
    -h, --help  show this help message and exit
    --foo FOO

If you would like to provide a different name for your argument in help messages, you can supply a value for the ``metavar`` keyword argument to :meth:`add_argument`::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo', metavar='YYY')
  >>> parser.add_argument('bar', metavar='XXX')
  >>> parser.parse_args('X --foo Y'.split())
  Namespace(bar='X', foo='Y')
  >>> parser.print_help()
  usage:  [-h] [--foo YYY] XXX
  
  positional arguments:
    XXX
  
  optional arguments:
    -h, --help  show this help message and exit
    --foo YYY

Note that ``metavar`` only changes the *displayed* name - the name of the attribute on the :meth:`parse_args` object is still determined by the dest_ value.

Different values of ``nargs`` may cause the metavar to be used multiple times.
If you'd like to specify a different display name for each of the arguments, you can provide a tuple to ``metavar``::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('-x', nargs=2)
  >>> parser.add_argument('--foo', nargs=2, metavar=('bar', 'baz'))
  >>> parser.print_help()
  usage: PROG [-h] [-x X X] [--foo bar baz]

  optional arguments:
    -h, --help     show this help message and exit
    -x X X
    --foo bar baz


dest
----

Most ArgumentParser actions add some value as an attribute of the object returned by :meth:`parse_args`. The name of this attribute is determined by the ``dest`` keyword argument of :meth:`add_argument`. For positional argument actions, ``dest`` is normally supplied as the first argument to :meth:`add_argument`::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('bar')
  >>> parser.parse_args('XXX'.split())
  Namespace(bar='XXX')

For optional argument actions, the value of ``dest`` is normally inferred from the option strings. ArgumentParser objects generate the value of ``dest`` by taking the first long option string and stripping away the initial ``'--'`` string.  If no long option strings were supplied, ``dest`` will be derived from the first short option string by stripping the initial ``'-'`` character.  Any internal ``'-'`` characters will be converted to ``'_'`` characters to make sure the string is a valid attribute name. The examples below illustrate this behavior::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('-f', '--foo-bar', '--foo')
  >>> parser.add_argument('-x', '-y')
  >>> parser.parse_args('-f 1 -x 2'.split())
  Namespace(foo_bar='1', x='2')
  >>> parser.parse_args('--foo 1 -y 2'.split())
  Namespace(foo_bar='1', x='2')

If you would like to use a different attribute name from the one automatically inferred by the ArgumentParser, you can supply it with an explicit ``dest`` parameter::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo', dest='bar')
  >>> parser.parse_args('--foo XXX'.split())
  Namespace(bar='XXX')
