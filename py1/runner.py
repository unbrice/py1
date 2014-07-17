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

"""Helps running user-provided code and getting readable backtraces."""

import sys
import traceback


class Error(Exception):

    """Base class for errors from this module."""


class RunFailed(Error):

    """The user-provided code failed."""

    def __init__(self, message):
        super(RunFailed, self).__init__(message)
        self.message = message


def build_globals():
    """Returns a dictionary that can be used as globals for exec."""
    return {
        '__name__': '__p1__',
        '__doc__': None,
        '__builtins__': __builtins__
    }


def _find_user_traceback_depth(tb):
    """Returns the depth of user-specific code in a traceback.

    This is the depth from wich we find a frame where __name__ is '__p1__'.

    Args:
      tb: A traceback object.
    """
    depth = 0
    while tb:
        # Find the topmost frame
        frame = tb.tb_frame
        while frame.f_back:
            frame = frame.f_back

        if frame.f_globals.get('__name__', None) != '__p1__':
            return depth + 1

        # If it does not contain '__p1__' go down the stack.
        depth += 1
        tb = tb.tb_next

    # We could not find it, assume everything was user-specified
    return 0


def _format_user_traceback(tb):
    """Returns the user-specific part of a traceback."""
    tb_depth = _find_user_traceback_depth(tb)
    # The limit keyword is counted from the top, we went the bottom.
    tb_list = traceback.extract_tb(tb, limit=None)
    return traceback.format_list(tb_list[tb_depth:])


def run(code, code_globals):
    """Runs the code with provided globals, improving backtraces readability.

    Args:
        code: The string or code object to run.
        code_globals: A dictionary that defines global and local variables.

    Raises:
      RunFailed: The user-provided code failed, the message will contain a clean backtrace.
    """
    try:
        exec(code, code_globals)
    except Exception as e:
        errors = []
        exc_type, exc_value, exc_tb = sys.exc_info()
        try:
            errors += _format_user_traceback(exc_tb)
        finally:
            del exc_tb  # Break the circular references early
        errors += traceback.format_exception_only(exc_type, exc_value)
        raise RunFailed(''.join(errors)) from e
    return None
