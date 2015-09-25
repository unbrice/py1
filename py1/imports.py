# Copyright (c) 2013-2015, Brice Arnould <unbrice@vleu.net>
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

"""Parses the import statements."""


class Error(Exception):

    """Base class for errors from this module."""


class BadShortSyntaxError(Error):

    """The user-provided code does not decode to valid code."""

    def __init__(self, short_import, expanded_import):
        msg ='Import statement %s means %s which is invalid.' % (
            short_import, expanded_import)
        super(BadShortSyntaxError, self).__init__(msg)
        self.short_import = short_import
        self.expanded_import = expanded_import


def expand_short(short_import):

    # from_str: the (optional) part between "from" and "import"
    if '/' in short_import:
        from_str, imported_str = short_import.split('/', 1)
    else:
        from_str, imported_str = None, short_import

    expanded_imported_str = imported_str.replace(':', ' as ')

    if from_str:
        res = 'from %s import %s' % (from_str, expanded_imported_str)
    else:
        res = 'import %s' % expanded_imported_str

    try:
        code = compile(res, '<py1:imports.expand_short>', 'exec')
    except SyntaxError:
        code = None

    if not code:
        raise BadShortSyntaxError(short_import, res)

    return res
