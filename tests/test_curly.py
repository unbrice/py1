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

"""Tests for the curly module."""

import threading
import unittest

from py1 import curly


class TestUnescape(unittest.TestCase):

    def testExec(self):
        samples = [
            # Most basic example
            'succeed()',
            # No whitespace
            'if True:{{succeed()}}',
            # Consecutive ifs
            'if True: {{ pass }} if True: {{ succeed() }}',
            # Inline ifs
            'if True: pass; if True: succeed()',
            # Nested ifs
            'if True: {{ if False: {{ pass }} else: {{ succeed() }} }}',
            # Strings
            '"}}" "{{" ; if True: {{ succeed() }}'
            # Dicts
            'd = {"ok": True} ; if d["ok"]: {{ succeed() }}',
            # Classes
            'class A(object): {{ def m(self): {{ succeed() }} }} ; A().m()',
            # Exceptions
            'try: {{ raise Exception() }} except: {{ succeed() }}',
        ]

        for sample in samples:
            event = threading.Event()
            test_globals = globals().copy()
            test_globals['succeed'] = event.set
            self.assertFalse(event.is_set())
            unescaped = curly.unescape(sample)
            code = compile(unescaped, '<test>', 'exec')
            exec(code, test_globals)
            self.assertTrue(event.is_set(), unescaped)

    def testCannotTokenize(self):
        samples = [
            # tokenize.TokenError
            '}',
            # IndentationError
            'if:\n  pass\n pass',
        ]
        for sample in samples:
            with self.assertRaises(curly.CannotTokenize) as cm:
                curly.unescape(sample)
            position = cm.exception.position
            self.assertIsInstance(position[0], int)
            self.assertIsInstance(position[1], int)

    def testMismatch(self):
        samples = ['{ { }}', '{{ } }']
        for sample in samples:
            with self.assertRaises(curly.Mismatch) as cm:
                curly.unescape(sample)
            token_and_pos = cm.exception.token_and_pos
            self.assertIsInstance(token_and_pos, curly.TokenAndPos)


if __name__ == '__main__':
    unittest.main()
