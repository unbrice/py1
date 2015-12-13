DESCRIPTION = "Runs awk-like Python one-liners."

LONG_DESCRIPTION = DESCRIPTION + """

py1 generates a python script wrapping your code.
You can use "{{ }}" instead of indentation, and ";" to separate statements:

The wrapper script can include a for loop that iterates on input lines.
"""

EPILOG="""examples:
  Shows first 8 powers of 2:
  $ py1 'for x in range(8): {{ P(2**x) }}'
  Counts empty lines:
  $ py1 'P(sum(1 if l else 0 for l in F))'
  Shows second and third fields of /etc/passwd:
  $ cat /etc/passwd | py1 -b 'WS=":"' -l 'P(W[1:2])'
  Sums key-value pairs:
  py1 -b 'd=defaultdict(int)' -l 'd[W[0]] += int(W[1])' -e 'P(d)'
"""

NAME = "py1"

VERSION = "0.3"
