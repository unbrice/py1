.. note: this file is also included by docs/index.rst


One should use the right tool for the right task. But Learning 300 tools is counterproductive, so one needs a fallback. To be generic enough that fallback must be scriptable. So we have AWK, Perl, Sed, TCL... and their read-only languages.

Enters **py1**, it aims at being a "Python AWK". It can be used in two modes.

In both modes indents and dedents can be replaced with “``{{``” and “``}}``”.

Minimalist
----------

You simply provide as a single argument the program with curly brackets.

.. code:: bash

    py1 "for x in range(4): {{ print x; print x*2 }}"

AWK-like
--------

You provide ``--begin``/``-b``, ``--each-line``/``-l``, ``--end``/``-e``. py1 generates a python script wrapping them and defining a convenient set of 1&2-letters variables and functions.

.. code:: bash

    py1 --begin "count=0" --each-line "if 'cow' in L: count += 1" --end "P(count)"

Sustainable hacking
-------------------

If you find yourself writing a longer than readable one-liner, you can
transform it in regular Python code, easily refactored for later reuse.
Just add ``--dump-code``.

More!
-----

Interested? You can install with "pip install py1".

To learn more you can read the
`list of one letter functions and variables <http://py1.vleu.net/page/variables.html>`_
or just look at
`examples <http://py1.vleu.net/page/examples.html>`_
and figure out the rest.

How to contribute?
------------------

I wrote some advices and documented the internals here. Feel free to
just `contact unbrice <mailto:unbrice@vleu.net>`_.