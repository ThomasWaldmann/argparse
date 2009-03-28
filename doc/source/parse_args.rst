The parse_args() method
=========================

.. method:: parse_args([args], [namespace])

   Convert the strings to objects and assign them as attributes of the namespace. Return the populated namespace.
   
   Previous calls to :meth:`add_argument` determine exactly what objects are created and how they are assigned. See the documentation for :meth:`add_argument` for details.
   
   By default, the arg strings are taken from ``sys.argv``, and a new empty ``Namespace`` object is created for the attributes.

Option value syntax
-------------------

The :meth:`parse_args` method supports several ways of specifying the value of an option (if it takes one). In the simplest case, the option and its value are passed as two separate arguments::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('-x')
  >>> parser.add_argument('--foo')
  >>> parser.parse_args('-x X'.split())
  Namespace(foo=None, x='X')
  >>> parser.parse_args('--foo FOO'.split())
  Namespace(foo='FOO', x=None)

For long options (options with names longer than a single character), you may also pass the option and value as a single command line argument, using ``=`` to separate them::

  >>> parser.parse_args('--foo=FOO'.split())
  Namespace(foo='FOO', x=None)

For short options (options only one character long), you may simply concatenate the option and its value::

  >>> parser.parse_args('-xX'.split())
  Namespace(foo=None, x='X')

You can also combine several short options together, using only a single ``-`` prefix, as long as only the last option (or none of them) requires a value::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('-x', action='store_true')
  >>> parser.add_argument('-y', action='store_true')
  >>> parser.add_argument('-z')
  >>> parser.parse_args('-xyzZ'.split())
  Namespace(x=True, y=True, z='Z')


Invalid arguments
-----------------

While parsing the command-line, ``parse_args`` checks for a variety of errors, including ambiguous options, invalid types, invalid options, wrong number of positional arguments, etc. When it encounters such an error, it exits and prints the error along with a usage message::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('--foo', type=int)
  >>> parser.add_argument('bar', nargs='?')
  
  >>> # invalid type
  >>> parser.parse_args(['--foo', 'spam'])
  usage: PROG [-h] [--foo FOO] [bar]
  PROG: error: argument --foo: invalid int value: 'spam'
  
  >>> # invalid option
  >>> parser.parse_args(['--bar'])
  usage: PROG [-h] [--foo FOO] [bar]
  PROG: error: no such option: --bar
  
  >>> # wrong number of arguments
  >>> parser.parse_args(['spam', 'badger'])
  usage: PROG [-h] [--foo FOO] [bar]
  PROG: error: extra arguments found: badger


Arguments containing ``"-"``
----------------------------

The ``parse_args`` method attempts to give errors whenever the user has clearly made a mistake, but some situations are inherently ambiguous. For example, the command-line arg ``'-1'`` could either be an attempt to specify an option or an attempt to provide a positional argument. The ``parse_args`` method is cautious here: positional arguments may only begin with ``'-'`` if they look like negative numbers and there are no options in the parser that look like negative numbers::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('-x')
  >>> parser.add_argument('foo', nargs='?')
  
  >>> # no negative number options, so -1 is a positional argument
  >>> parser.parse_args(['-x', '-1'])
  Namespace(foo=None, x='-1')
  
  >>> # no negative number options, so -1 and -5 are positional arguments
  >>> parser.parse_args(['-x', '-1', '-5'])
  Namespace(foo='-5', x='-1')
  
  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('-1', dest='one')
  >>> parser.add_argument('foo', nargs='?')
  
  >>> # negative number options present, so -1 is an option
  >>> parser.parse_args(['-1', 'X'])
  Namespace(foo=None, one='X')
  
  >>> # negative number options present, so -2 is an option
  >>> parser.parse_args(['-2'])
  usage: PROG [-h] [-1 ONE] [foo]
  PROG: error: no such option: -2
  
  >>> # negative number options present, so both -1s are options
  >>> parser.parse_args(['-1', '-1'])
  usage: PROG [-h] [-1 ONE] [foo]
  PROG: error: argument -1: expected one argument

If you have positional arguments that must begin with ``'-'`` and don't look like negative numbers, you can insert the pseudo-argument ``'--'`` which tells ``parse_args`` that everything after that is a positional argument::

  >>> parser.parse_args(['--', '-f'])
  Namespace(foo='-f', one=None)


Argument abbreviations
----------------------

The :meth:`parse_args` method allows you to abbreviate long options if the abbreviation is unambiguous::

  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('-bacon')
  >>> parser.add_argument('-badger')
  >>> parser.parse_args('-bac MMM'.split())
  Namespace(bacon='MMM', badger=None)
  >>> parser.parse_args('-bad WOOD'.split())
  Namespace(bacon=None, badger='WOOD')
  >>> parser.parse_args('-ba BA'.split())
  usage: PROG [-h] [-bacon BACON] [-badger BADGER]
  PROG: error: ambiguous option: -ba could match -badger, -bacon

As you can see above, you will get an error if you pick a prefix that could refer to more than one option.


Beyond ``sys.argv``
-------------------

Sometimes it may be useful to have an ArgumentParser parse args other than those of ``sys.argv``.  This can be accomplished by passing a list of strings to ``parse_args``.  You may have noticed that the examples in the argparse documentation have made heavy use of this calling style - it is much easier to use at the interactive prompt::

  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument(
  ...     'integers', metavar='int', type=int, choices=xrange(10),
  ...  nargs='+', help='an integer in the range 0..9')
  >>> parser.add_argument(
  ...     '--sum', dest='accumulate', action='store_const', const=sum,
  ...   default=max, help='sum the integers (default: find the max)')
  >>> parser.parse_args(['1', '2', '3', '4'])
  Namespace(accumulate=<built-in function max>, integers=[1, 2, 3, 4])
  >>> parser.parse_args('1 2 3 4 --sum'.split())
  Namespace(accumulate=<built-in function sum>, integers=[1, 2, 3, 4])


Custom namespaces
-----------------

It may also be useful to have an ArgumentParser assign attributes to an already existing object, rather than the newly-created Namespace object that is normally used. This can be achieved by specifying the ``namespace=`` keyword argument::

  >>> class C(object):
  ...     pass
  ...    
  >>> c = C()
  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo')
  >>> parser.parse_args(args=['--foo', 'BAR'], namespace=c)
  >>> c.foo
  'BAR'
