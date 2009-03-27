Introduction to argparse
========================

Pretty much every script that uses the argparse module will start out by creating an :class:`ArgumentParser` object. Typically, this will look something like::

  >>> parser = argparse.ArgumentParser(description='Frabble the foo and the bars')

The :class:`ArgumentParser` object will hold all the information necessary to parse the command line into a more manageable form for your program.


Adding arguments
----------------

Once you've created an :class:`ArgumentParser`, you'll want to fill it with information about your program arguments. You typically do this by making calls to the :meth:`add_argument` method.  Generally, these calls tell the :class:`ArgumentParser` how to take the strings on the command line and turn them into objects for you. This information is stored and used when :meth:`parse_args` is called. For example, if we add some arguments like this::

  >>> parser.add_argument('-f', '--foo', action='store_true', help='frabble the foos')
  >>> parser.add_argument('bar', nargs='+', type=int, help='a bar to be frabbled')

when we later call :meth:`parse_args`, we can expect it to return an object with two attributes, ``foo`` and ``bar``.  The ``foo`` attribute will be ``True`` if ``--foo`` was supplied at the command-line, and the ``bar`` attribute will be a list of ints determined from the remaining command-line arguments::

  >>> parser.parse_args('--foo 1 2 3 5 8'.split())
  Namespace(bar=[1, 2, 3, 5, 8], foo=True)

As you can see from the example above, calls to :meth:`add_argument` start with either a single string name for positional arguments or a series of option strings (beginning with ``'-'``) for optional arguments.  The remaining keyword arguments to :meth:`add_argument` specify exactly what sort of action should be carried out when the :class:`ArgumentParser` object encounters the corresponding command-line args.  So in our example above, we are telling the :class:`ArgumentParser` object that when it encounters ``--foo`` in the command-line args, it should invoke the ``'store_true'`` action.


Parsing arguments
-----------------

Once an :class:`ArgumentParser` has been initialized with appropriate calls to :meth:`add_argument`, it can be instructed to parse the command-line args by calling the :meth:`parse_args` method.  This will inspect the command-line, convert each arg to the appropriate type and then invoke the appropriate action.  In most cases, this means a simple namespace object will be built up from attributes parsed out of the command-line.

In the most common case, :meth:`parse_args` will be called with no arguments, and the :class:`ArgumentParser` will determine the command-line args from ``sys.argv``.  The following example sets up a simple :class:`ArgumentParser` and then calls :meth:`parse_args` in this manner::

  import argparse
  
  if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      'integers', metavar='int', type=int, choices=xrange(10),
       nargs='+', help='an integer in the range 0..9')
  parser.add_argument(
      '--sum', dest='accumulate', action='store_const', const=sum,
    default=max, help='sum the integers (default: find the max)')
  
  args = parser.parse_args()
  print args.accumulate(args.integers)

Assuming this program is saved in the file ``script.py``, the call to :meth:`parse_args` means that we get the following behavior when running the program from the command-line::

  $ script.py 1 2 3 4
  4
  
  $ script.py --sum 1 2 3 4
  10

That's pretty much it. You're now ready to go write some command line interfaces!
