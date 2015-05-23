DESCRIPTION = "Enables one to write Python one-liners."

LONG_DESCRIPTION = DESCRIPTION + """

Can be used in two modes:
 - awk-like: you provide --begin/-b, --each-line/-l, --end/-e and py1 generates
   and run a python script wrapping them.
 - minimalist: you provide a single argument a Python program

In both modes indents and dedents can be replaced with "{{" and "}}".
"""

EPILOG="""examples:
  Shows first 8 powers of 2:
  $ py1 -b 'for x in range(8): {{ P(2**x) }}'
  Counts empty lines:
  $ py1 -e 'P(sum(1 if l else 0 for l in F))'
  Shows second and third fields of /etc/passwd:
  $ cat /etc/passwd | py1 -b 'WS=":"' -l 'P(W[1:2])'
  Sums key-value pairs:
  py1 -b 'd=defaultdict(int)' -l 'd[W[0]] += int(W[1])' -e 'P(d)'
"""

NAME = "py1"

VERSION = "0.1"
