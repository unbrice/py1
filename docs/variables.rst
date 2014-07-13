Convenience variables
=====================

Follows a list of all the functions and variables you can use in Awk-like mode.

.. warning::

  These variables are available in Awk-like mode, that is when ``--begin``/``-b``, ``--each-line``/``-l``, ``--end``/``-e`` have been passed.
  It is enough to pass any of the above to get them so ``py1 -b 'P(42)'`` works.


Per-line
--------

.. list-table::
   :header-rows: 1

   * - Name
     - Description
     - Type
   * - L
     - The current line, stripped
     - :py:class:`str`
   * - R
     - The raw current line
     - :py:class:`str`
   * - LN
     - The current line number
     - :py:class:`int`
   * - W
     - Words of L split on WS or WRE
     - :py:class:`str`
   * - NW
     - Length of W
     - :py:class:`int`

Global
------

These are defined in the whole program.

.. list-table::
   :header-rows: 1

   * - Name
     - Usage
     - Default
     - Type
   * - ENV
     - Maps names to values of environment variables
     - :py:data:`os.environ`
     - {:py:class:`str`: :py:class:`str`}

Input
~~~~~

.. list-table::
   :header-rows: 1

   * - Name
     - Usage
     - Default
     - Type
   * - F
     - The input file
     - :py:data:`sys.stdin`
     - file (:py:class:`io.FileIO`)
   * - WS
     - Word separator, ignored if WRE is set
     - Any whitespace
     - :py:class:`str`
   * - WRE
     - Word RegExp separator
     - :py:const:`None`
     - :py:class:`str` or :py:mod:`re`

Output
~~~~~~

.. list-table::
   :header-rows: 1

   * - Name
     - Usage
     - Default
     - Type
   * - OF
     - The output file
     - :py:data:`sys.stdout`
     - file (:py:class:`io.FileIO`)
   * - OWS
     - Output Word Separator
     - space
     - :py:class:`str`
   * - OLS
     - Output Line Separator
     - \\n
     - :py:class:`str`

Functions
---------

.. autofunction:: py1.user_code_template.P
.. autofunction:: py1.user_code_template.M
.. autofunction:: py1.user_code_template.S

