.. highlight:: bash


Imports
=======

``--i``/``--import`` is a shortcut to easily import external libraries.

Importing a module
------------------

The equivalent of ``import xyz`` is ``--import xyz``.
It is equivalent to ``--begin import xyz``, just shorter.
You can use ``-i xyz`` which is even shorter.

.. code:: bash

    py1 --begin 'import math' 'P(math.cos(math.pi))'
    py1 --import 'math' 'P(math.cos(math.pi))'
    py1 -i 'math' 'P(math.cos(math.pi))'

Importing specific symbols
--------------------------

The equivalent of ``from xyz import abc`` is ``--import xyz/abc``.
You can import multiple functions with ``--import xyz/abc,def``.
Something like ``-i xyz/*`` is equivalent to ``from xyz import *``.

.. code:: bash

    py1 --import 'math/cos,pi' 'P(cos(pi))'
    py1 -i 'math/*' 'P(cos(pi))'


Importing with a specific name
------------------------------

The equivalent of ``import abc as ABC`` is ``--import abc:ABC``. You can rename specific symbols in the same way like ``--import xyz/abc:ABC``.

.. code:: bash

    py1 --import 'math:M' 'P(M.cos(M.pi))'
