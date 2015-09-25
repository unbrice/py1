:orphan:

py1 manual page
===============

Synopsis
--------

**py1** < [-b *BEGIN*] [-l *EACH_LINE*] [-e *END*] | *single_snippet* >

Description
-----------
Runs awk-like Python one-liners. Provides convenience functions, "{{ }}" can be used instead of indent/dedent.


Usage
-----

py1 generates a python script wrapping your code. You can use "{{ }}" instead of indentation, and ";" to separate statements:

   **py1** "import sys ; if True: {{ print(sys.version) }}"

The wrapper script defines a convenient set of 1&2-letters variables and functions.   
It can also include a for loop that iterates on input lines. To get the for loop, pass **--each-line**/**-l**.

For example, to count lines matching '$a*^':

.. code:: bash

   py1 --begin "count=0" --each-line "if M('$a*^'): count += 1"
       --end "P(count)"

If in doubt, **--code** shows the generated code.

For more examples, please see `http://py1.vleu.net/examples.html`. For the definition of all 1&2-letters helpers, please refer to `http://py1.vleu.net/variables.html`. 

Options
-------

  -h, --help  show an help message and exit

  -i IMPORT, --import IMPORT  imports modules described in abbreviated form

  -b CODE, --begin CODE  code run once first

  -e CODE, --end CODE  code run once at the end
  
  -l CODE, --each-line CODE  code run each line

  -c <full|concise>, --code <full|concise>
    show the code that would have run, abbreviated or not
  
  -V, --version  show program's version number and exit
