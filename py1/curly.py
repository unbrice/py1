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

"""Implements the un-escaping of the {{ }} indents."""

import collections
import io
import tokenize


class Token(collections.namedtuple('_Token', 'num val')):

    """Represents a single Token.

    Attributes:
        num: The token type as per the tokenize module.
        val: The token value as per the tokenize module.
    """


class TokenAndPos(collections.namedtuple('_TokenAndPost', 'token start end')):

    """Represents a single Token and its position.

    Attributes:
        token: A Token object.
        start: a (row, col) tuple specifying where the token begins.
        end: a (row, col) tuple specifying where the token ends.
    """


class Error(Exception):

    """Base class for errors from this module."""


class Mismatch(Error):

    """There is not the same number of '{{' and '}}'."""

    def __init__(self, message, token_and_pos):
        super(Mismatch, self).__init__(message)
        self.message = message
        self.token_and_pos = token_and_pos


class CannotTokenize(Error):

    """Raised when the tokenize module failed."""

    def __init__(self, message, position):
        super(CannotTokenize, self).__init__(message)
        self.message = message
        self.position = position


_DEDENT_TOKEN = Token(tokenize.OP, '}')
_INDENT_TOKEN = Token(tokenize.OP, '{')
_NL_TOKEN = Token(tokenize.OP, ';')


def _unescape_tokens(tokens):
    """Substitutes '{{' by tokenize.INDENT and '}}' by tokenize.DEDENT.

    Args:
      tokens: 5-tupples as returned by tokenize.generate_tokens.

    Returns:
      Token objects.
    """
    eat_next_token = False
    level = 0
    for toknum, tokval, tokstart, tokend, tokline in tokens:
        if eat_next_token:
            eat_next_token = False
            continue

        token = Token(toknum, tokval)
        token_and_pos = TokenAndPos(token=token, start=tokstart, end=tokend)
        next_char_start = tokstart[1] + 1
        if tokline and len(tokline) > next_char_start:
            next_char = tokline[next_char_start]
        else:
            next_char = None

        if token == _NL_TOKEN:
            yield (tokenize.NEWLINE, '\n')
        elif (token, next_char) == (_INDENT_TOKEN, _INDENT_TOKEN.val):
            level += 1
            eat_next_token = True
            yield (tokenize.NEWLINE, '\n')
            yield (tokenize.INDENT, '  ' * level)
        elif (token, next_char) == (_DEDENT_TOKEN, _DEDENT_TOKEN.val):
            if not level:
                raise Mismatch('More "}}" than "{{"', token_and_pos)
            level -= 1
            eat_next_token = True
            yield (tokenize.NEWLINE, '\n')
            yield (tokenize.DEDENT, '  ' * level)
        else:
            yield token
    if level:
        raise Mismatch('More "{{" than "}}"', token_and_pos)


def unescape(code_str):
    """Substitutes '{{' by indents and '}}' by dedents.

    Args:
      code_str: The 1-line Python snippet.

    Returns:
      Standard valid Python as a string.

    Raises:
      Error: The conversion failed.
    """
    code_file = io.StringIO(code_str)
    tokens = tokenize.generate_tokens(code_file.readline)
    try:
        unescaped_tokens = list(_unescape_tokens(tokens))
        return tokenize.untokenize(unescaped_tokens)
    except tokenize.TokenError as e:
        raise CannotTokenize(message=e.args[0], position=e.args[1])
    except IndentationError as e:
        raise CannotTokenize(message=e.args[0],
                             position=(e.args[1][1], e.args[1][2]))
