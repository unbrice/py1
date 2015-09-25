.. image:: https://readthedocs.org/projects/py1/badge/?version=latest
    :target: http://py1.vleu.net

.. image:: https://travis-ci.org/unbrice/py1.svg?branch=master
    :target: https://travis-ci.org/unbrice/py1

.. image:: https://coveralls.io/repos/unbrice/py1/badge.png?branch=master
  :target: https://coveralls.io/r/unbrice/py1?branch=master

.. image:: https://gemnasium.com/unbrice/py1.svg
    :target: https://gemnasium.com/unbrice/py1

Tutorial
========


This is an excerpt, you can find the `full documentation on ReadTheDocs <http://py1.vleu.net/>`_.

.. FILTER_DOC_BEFORE_THIS_LINE
.. note: this file is also included by docs/index.rst, from this line onwards

Installation
------------

To install from `Pypi <https://pypi.python.org/pypi/py1cmd>`_: 

.. code-block:: bash

    pip install py1cmd

Introduction
------------

One should use the right tool for the right task. But Learning 300 tools is counterproductive, so one needs a fallback. To be generic enough that fallback must be scriptable. So we have AWK, Perl, Sed, TCL... and their read-only languages.

Enters **py1**, it aims at being a "Python AWK".

Indents and dedents can be replaced with ``{{`` and ``}}``, line feeds can be replaced with ``;``. An optional for loop iterates on input lines.

Usage
-----

Using ``{{`` ``}}`` instead of indentation, and ``;`` to separate statements:

.. code-block:: bash

   py1 "a = 1+2; if a > 4: {{ print(a) }}"


The wrapper script defines a convenient set of 1&2-letters variables and functions.
It can also include a for loop that iterates on input lines. To get the for loop, pass ``--each-line``/``-l``.

For example, to count lines matching ``'$a*^'``:

.. code-block:: bash

    py1 --begin "count=0" --each-line "if M('$a*^'): count += 1"
        --end "P(count)"

Lastly the wrapper script provide a short notation to easily import modules.

.. code-block:: bash

    py1 --import "math/*" "P(cos(pi))"

To learn more you can read the
`list of one letter functions and variables <http://py1.vleu.net/page/variables.html>`_
or just look at
`examples <http://py1.vleu.net/page/examples.html>`_
and figure out the rest.


Sustainable hacking
-------------------

If you find yourself writing a longer than readable one-liner, you can
transform it in regular Python code, easily refactored for later reuse.
Just add ``--code=full``.

More!
-----

Interested? You can install with:

.. code-block:: bash

    pip install py1cmd


To learn more you can read the
`list of one letter functions and variables <http://py1.vleu.net/page/variables.html>`_
or just look at
`examples <http://py1.vleu.net/page/examples.html>`_
and figure out the rest.


How to contribute?
------------------

I wrote some advices and documented the internals here. Feel free to
just `contact unbrice <mailto:unbrice@vleu.net>`_.
