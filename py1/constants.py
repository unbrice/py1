DESCRIPTION = "Enables one to write Python one-liners."

LONG_DESCRIPTION = DESCRIPTION + """

Can be used in two modes:
 - awk-like: you provide --begin/-b, --each-line/-l, --end/-e and it generates and run a python script wrapping them.
 - minimalist: you provide a single argument a Python program

In both modes indents and dedents can be replaced with "{{" and "}}".
"""

NAME = "py1"

VERSION = "0.1"
