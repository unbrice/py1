"""This file is used as a base for generated script.

As it is checked in, it defines a mostly no-op program, with placeholders
that get replaced with the user-defined code.
Having in this form allows to test it, and document it more easily.
"""

# Monkey patch stdin to make autodoc work.
import io
import sys
sys.stdin = io.StringIO('Monkey patched stdin from %s' % __name__)
# Everything after this is removed when the user-script is generated.
# __________ REMOVE EVERYTHING ABOVE __________
import re
import sys
import os
from collections import defaultdict

# Program conveniency variables.
ENV = os.environ   # ENV: dict of Environment strings
# Input
F = sys.stdin    # F: input File, defaults to stdin
WS = None        # WS: Word Separator, defaults to whitespace
WRE = None       # WS: Word RegExp separator, overrides WS if set
# Output
OF = sys.stdout  # OF: Output File, defaults to stdin
OWS = None       # OWS: Output Word Separator, defaults to whitespace
OLS = None       # OLS: Output Line Separator, defaults to \\n


def P(*args, **kwargs):
    """Like :py:func:`print()` but honors OWS, OLS & OF."""
    kwargs.setdefault("sep", OWS)
    kwargs.setdefault("end", OLS)
    kwargs.setdefault("file", OF)
    print(*args, **kwargs)


def M(pattern, string=None, flags=0):
    """Returns all capture groups starting with the full match.

    Args:
      pattern (str): The regexp to match on.
      string (str): The string that will be matched, default to the full line
        (the `R` variable).
      flags (int): Matching option as per :py:func:`re.match`

    Returns:
      tuple(str) or None: Capture groups, starting with the full match; or None
        if there were no match.
    """
    string = R if string is None else string
    matched = re.search(pattern, string, flags)
    if matched is None:
        return None
    return (matched.group(0), ) + matched.groups()


def S(pattern, repl, string=None, count=0, flags=0):
    """Substitute pattern with repl in string (or R if string is None).

    Args:
      pattern (str): The regexp to match on.
      repl (str): The string to substitute the matches with.
      string (str): The string that will be matched, default to the full line
        (the `R` variable).
      count (int): Replace at most that many occurences.
      flags (int): Matching option as per :py:func:`re.sub`

    Returns:
      str: The string after substitutions.
    """
    string = R if string is None else string
    return re.sub(pattern, repl, string, count, flags)

# __________ INSERT USER CODE FOR --begin HERE __________

# LN: Line Number; R: Raw Line
for LN, R in enumerate(F):
    # Line conveniency variables.
    L = R.strip()           # L: Line without whitespace arround.
    if WRE is None:
        W = L.split(WS)       # W: Words split on WS
    else:
        W = re.split(WRE, L)  # W: Words split on WRE
    NW = len(W)             # Number of words
    # __________ INSERT USER CODE FOR --each-line HERE __________

# __________ INSERT USER CODE FOR --end HERE __________
