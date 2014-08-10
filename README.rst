Introduction
------------

.. image:: https://travis-ci.org/unbrice/py1.svg?branch=master
    :target: https://travis-ci.org/unbrice/py1

.. image:: https://coveralls.io/repos/unbrice/py1/badge.png?branch=master
  :target: https://coveralls.io/r/unbrice/py1?branch=master

.. image:: https://gemnasium.com/unbrice/py1.svg
    :target: https://gemnasium.com/unbrice/py1

This is an excerpt, you can find the `full documentation on ReadTheDocs <http://py1.vleu.net/>`_.

.. FILTER_SPHINX_DOC_BEFORE_THIS_LINE
.. note: this file is also included by docs/index.rst, from this line onwards

One should use the right tool for the right task. But Learning 300 tools is counterproductive, so one needs a fallback. To be generic enough that fallback must be scriptable. So we have AWK, Perl, Sed, TCL... and their read-only languages.

Enters **py1**, it aims at being a "Python AWK". It can be used in two modes.

In both modes indents and dedents can be replaced with “``{{``” and “``}}``”, line feeds can be replaced with “``;``”.

Minimalist
----------

To use this mode:

.. code-block:: bash

   py1 "python_one_liner"

"{{" and "}}" can be used instead of indent/dedent, and ";" instead of line feed eg:

.. code-block:: bash

   py1 "import sys ; if True: {{ print(sys.version) }}"


AWK-like
--------

In this mode, py1 generates a python script wrapping your code and defining a convenient set of 1&2-letters variables and functions.

To use this mode, pass any of ``--begin``/``-b``, ``--each-line``/``-l``, ``--end``/``-e``.

For example, to count lines matching ``'$a*^'``:

.. code-block:: bash

    py1 --begin "count=0" --each-line "if M('$a*^'): count += 1"
        --end "P(count)"

To learn more you can read the
`list of one letter functions and variables <http://py1.vleu.net/page/variables.html>`_
or just look at
`examples <http://py1.vleu.net/page/examples.html>`_
and figure out the rest.


Sustainable hacking
-------------------

If you find yourself writing a longer than readable one-liner, you can
transform it in regular Python code, easily refactored for later reuse.
Just add ``--dump-code``.

More!
-----

Interested? You can install with "pip install py1cmd".

To learn more you can read the
`list of one letter functions and variables <http://py1.vleu.net/page/variables.html>`_
or just look at
`examples <http://py1.vleu.net/page/examples.html>`_
and figure out the rest.


How to contribute?
------------------

I wrote some advices and documented the internals here. Feel free to
just `contact unbrice <mailto:unbrice@vleu.net>`_.
