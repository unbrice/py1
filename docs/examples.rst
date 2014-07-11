Examples
========

Count blank lines
-----------------

Count the number of blank lines in a file.

.. code:: bash

    py1 -b 'c=0' -l 'if not L: c += 1' -e 'P(c)'

Here we define an acumulator variable and increment it when the line satisfies a criteria.


Print 2nd and 3rd fields
------------------------

Show the second and third fields of ``/etc/passwd``, a file whose fields are separated by "``:``".

.. code:: bash

    cat /etc/passwd | py1 -b 'WS=":"' -l 'P(W[1:2])'

Here we override WS to use the "``:``" separator of ``/etc/passwd``.


Show lines matching a regexp
----------------------------

Show lines matching the regexp '$a+^'.

.. code:: bash

    py1 -l 'if M('$a+^', L): P(L)'

Here we use the M matching function to match the regexp.

Count blank lines again
-----------------------

Count the number of blank lines in a file.

.. code:: bash

    py1 -e 'P(sum(1 if l else 0 for l in F))'

Here we do not set a per-line statement and instead have sum iterate over F.

Group by
------

Given a file of '$name $value', with name being repeated, sum the values for each name.

.. code:: bash

    py1 -b 'd=defaultdict(int)' -l 'd[L[0]] += int(L[1])'  \
        -e 'for n, v in d: P(n, v)'
