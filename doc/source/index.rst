Documentation
=============

.. toctree::
   :maxdepth: 2

   overview
   argparse-vs-optparse
   api-docs


Example usage
=============

The following simple example uses the argparse module to generate the command-line interface for a Python program that sums its command-line arguments and writes them to a log file::

  import argparse
  import sys
  
  if __name__ == '__main__':
  
      # create the parser    
      parser = argparse.ArgumentParser(
          description='Sum the integers on the command line.')
  
      # add the arguments    
      parser.add_argument(
          'integers', metavar='int', type=int, nargs='+',
          help='one of the integers to be summed')
      parser.add_argument(
          '--log', type=argparse.FileType('w'), default=sys.stdout,
          help='the file where the sum should be written '
               '(default: write the sum to stdout)')
  
      # parse the command line    
      args = parser.parse_args()
  
      # write out the sum
      args.log.write('%s\n' % sum(args.integers))
      args.log.close()


Assuming the Python code above is saved into a file called ``scriptname.py``, it can be run at the command line and provides useful help messages::

  $ scriptname.py -h
  usage: scriptname.py [-h] [--log LOG] int [int ...]
  
  Sum the integers on the command line.
  
  positional arguments:
    int         one of the integers to be summed
  
  optional arguments:
    -h, --help  show this help message and exit
    --log LOG   the file where the sum should be written (default: write the sum
                to stdout)


When run with the appropriate arguments, it writes the sum of the command-line integers to the specified log file::

  $ scriptname.py --log=log.txt 1 1 2 3 5 8
  $ more log.txt
  20
