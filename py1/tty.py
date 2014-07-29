# Copyright (c) 2013, Brice Arnould <unbrice@vleu.net>
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following condition are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Functions for making the most of a TTY."""

import curses
import os
import sys
import tempfile
import traceback


class Error(Exception):

    """Base class for errors from this module."""


def count_ansi_colors(term_name=None):
    """Counts ANSI-coded colors a terminal supports.

    Bug: Subsequent calls might return the same value as the first if terminfo
    has to be used that is when term_info is not in 'xterm-256colors', 'xterm',
    'unknown'.

    Args:
      term_name (str): A string like 'xterm' or 'unknown', defaults to the
        environment value for TERM.

    Returns:
      int: Number of ANSI-coded colors the terminal supports.
    """
    if term_name is None:
        term_name = os.getenv('TERM')

    # We hardcode a few values as curses does not reload terminfo on subsequent
    # calls to setupterm and terminfo often is mis-installed.
    if term_name.endswith('-256color'):
        return 256
    if term_name.endswith('-16color'):
        return 16
    elif term_name in ['xterm', 'hterm', 'screen']:
        return 8
    elif term_name == 'unknown':
        return 0

    try:
        # We have to provide a temporary file as the fd to prevent ncurses from
        # messing with the terminal.
        with tempfile.NamedTemporaryFile() as f:
            curses.setupterm(term_name, f.fileno())
        for capability in ('setaf', 'setab', 'bold'):
            if not curses.tigetstr(capability):
                # If we get here it means the terminal support colors but not
                # through ANSI color sequences.
                return 0
    except curses.error:
        return 0

    return curses.tigetnum("colors")


def ansi_highlight_code(python_code, ansi_colors):
    """Adds ANSI color code to make python_code pretty.

    Args:
      python_code (str): Python 3 code to prettify.
      ansi_colors (int): Number of colors to use, as returned by
          count_ansi_colors().

    Returns:
      str: The prettified Python code.
    """
    import pygments
    import pygments.lexers
    import pygments.formatters

    if ansi_colors >= 256:
        formatter = pygments.formatters.Terminal256Formatter(bg='dark')
    elif ansi_colors >= 8:
        formatter = pygments.formatters.TerminalFormatter(bg='dark')
    else:
        return python_code

    lexer = pygments.lexers.get_lexer_by_name('python3')
    return pygments.highlight(python_code, lexer, formatter)
