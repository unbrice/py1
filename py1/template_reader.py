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

"""The template with the conveniency variables."""

import pkgutil
import optparse
import os
import sys
import warnings

from py1 import curly
from py1 import runner


_FOR_LINE_INDENT = ' ' * 4


class Error(Exception):

    """Base class for errors from this module."""


class InvalidTemplateError(Error):

    """Raised by build_code when the template is invalid."""


def _get_template():
    """Returns the content of user_template_reader.py as a utf-8 string."""
    # pkgutil.get_data triggers a ResourceWarnin'g on Python 3.2
    if sys.version_info[:2] == (3, 2):
        warnings.simplefilter('ignore', ResourceWarning)
    bytes = pkgutil.get_data(__name__, 'user_code_template.py')
    return bytes.decode('utf-8')


def _read_template_until(iterator, searched):
    """Reads iterator until we find `searched`.

    Args:
      iterator: Will be consumed until we find `searched`.
      searched (str): The string we are looking for.

    Returns:
        list(str): Consumed elements from `iterator`.

    Raises:
      InvalidTemplateError: Could not find `searched`.
    """
    result = []
    for s in iterator:
        if s == searched:
            return result
        result.append(s)

    raise InvalidTemplateError('Could not find "%s"' % searched)


def build_code(begin, each_line, end):
    """Instantiates the templates running the specified code.

    Args:
      begin: List of strings, will be run before the main loop.
      each_line: List of strings, will be run in the main loop.
      end: List of strings, will be run just after the main loop.
    """
    result = []

    # An iterator over the template's line. We advance it while consuming.
    reader = iter(_get_template().splitlines())

    # Start discarding everything above the code.
    _read_template_until(
        reader, '# __________ REMOVE EVERYTHING ABOVE __________')

    result.extend(_read_template_until(
        reader, '# __________ INSERT USER CODE FOR --begin HERE __________'))
    if begin:
        result.append('## --begin')
        result += begin
        result.append('')

    for_loop = _read_template_until(
        reader, _FOR_LINE_INDENT +
        '# __________ INSERT USER CODE FOR --each-line HERE __________')
    if each_line:
        result.extend(for_loop)
        for s in each_line:
            result.append(_FOR_LINE_INDENT + '## --each-line')
            result.append(_FOR_LINE_INDENT
                          + s.replace('\n', '\n' + _FOR_LINE_INDENT))
            result.append('')

    result.extend(_read_template_until(
        reader, '# __________ INSERT USER CODE FOR --end HERE __________'))
    if end:
        result.append('## --end')
        result += end
        result.append('')

    result.extend(reader)

    return '\n'.join(result)
