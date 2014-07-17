# Copyright (c) 2014, Brice Arnould <unbrice@vleu.net>
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

"""Tests for the user template module."""

import io
import unittest
try:
    from unittest import mock
except ImportError:
    # Allows compatibility with Python < 3.3 if mock is installed.
    import mock
import sys

from py1 import user_code_template


class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.addCleanup(mock.patch.stopall)

    def testP(self):
        """Validates the P() function."""
        # Checks P() honors OWS, OLS and OF
        with io.StringIO() as f:
            with mock.patch.multiple(user_code_template, OWS='-', OLS='*', OF=f):
                user_code_template.P('a', 'b')
                user_code_template.P('c', 'd')
            self.assertEqual('a-b*c-d*', f.getvalue())

        # Checks P() honors OWS, OLS and OF
        with io.StringIO() as f:
            user_code_template.P('a', 'b', sep=',', end='+', file=f)
            user_code_template.P('c', 'd', sep=',', end='+', file=f)
            self.assertEqual('a,b+c,d+', f.getvalue())

    def testM(self):
        """Validates the M() function."""
        # No match should result in none to returned
        self.assertIsNone(user_code_template.M('abc', 'def'))
        # We should otherwise get all capture groups
        self.assertEqual(('a b', 'a', 'b'),
                         user_code_template.M(r'(a) (b)', 'a b'))
        # And that should be applied to R if no string is present.
        with mock.patch.object(user_code_template, 'R', 'a b'):
            self.assertEqual(('a b', 'a', 'b'),
                             user_code_template.M(r'(a) (b)'))

    def testS(self):
        """Validates the S() function."""
        # We should replace all instances
        self.assertEqual('py1 py1',
                         user_code_template.S(r'\w+', 'py1', 'awk sed'))
        # And that should be applied to R if no string is present.
        with mock.patch.object(user_code_template, 'R', 'cat grep'):
            self.assertEqual('py1 py1', user_code_template.S(r'\w+', 'py1'))


if __name__ == '__main__':
    unittest.main()
