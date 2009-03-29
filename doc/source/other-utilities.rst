Other utilities
===============

FileType objects
----------------

.. class:: FileType(mode='r', bufsize=None)

   The :class:`FileType` factory creates objects that can be passed to the type argument of :meth:`add_argument`. Arguments that have :class:`FileType` objects as their type will open command-line args as files with the requested modes and buffer sizes:
   
   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--output', type=argparse.FileType('wb', 0))
   >>> parser.parse_args(['--output', 'out'])
   Namespace(output=<open file 'out', mode 'wb' at 0x...>)
   
   FileType objects understand the pseudo-argument ``'-'`` and automatically convert this into ``sys.stdin`` for readable :class:`FileType` objects and ``sys.stdout`` for writable :class:`FileType` objects:
   
   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('infile', type=argparse.FileType('r'))
   >>> parser.parse_args(['-'])
   Namespace(infile=<open file '<stdin>', mode 'r' at 0x...>)
