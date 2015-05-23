:orphan:

py1 manual page
===============

Synopsis
--------

**py1** < [-b *BEGIN*] [-e *END*] [-l *EACH_LINE*] | *python_one_liner* >

Description
-----------
Enables one to write Python one-liners. It is meant to be used in interactive shell sesssions and provide a slightly augmented Python language where {{ }} can be used instead of indent/dedent.

Minimalist mode
---------------

To use this mode:

   **py1** *python_one_liner*

"{{" and "}}" can be used instead of indent/dedent, and ";" instead of line feed eg:

   **py1** "import sys ; if True: {{ print(sys.version) }}"


Awk-like mode
-------------

In this mode, py1 generates a python script wrapping your code and defining a convenient set of 1&2-letters variables and functions.

To use this mode, pass any of **-b**/**--begin**, **-l**/**--each-line**, **-e**/**--end**.

For example, to count lines matching '$a*^':

.. code:: bash

   py1 --begin "count=0" --each-line "if M('$a*^'): count += 1"
       --end "P(count)"

For more examples, please see `http://py1.vleu.net/examples.html`, for the definition of all 1-letter varibles, please refer to `http://py1.vleu.net/variables.html`. 

Options
-------
  
  -h, --help             show an help message and exit

  -b PY, --begin PY      code run once first

  -e PY, --end PY        code run once at the end
  
  -l PY, --each-line PY  code run each line

  -c, --code             show the code that would have run, abbreviated

  -c=full, --code=full   show the entirety of the code that would have run
  
  -V, --version          show program's version number and exit
