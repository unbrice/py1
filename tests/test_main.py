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

"""Tests for the main module.

De facto they serve as integration tests.
"""

import io
import unittest
from unittest import mock 
import sys

from py1 import constants
from py1 import main
from py1 import runner

class TestMain(unittest.TestCase):

    def setUp(self):
        self.addCleanup(mock.patch.stopall)
        self.stderr = io.StringIO()
        self.stdout = io.StringIO()

    def ioPatcher(self):
        return mock.patch.multiple(sys, stderr=self.stderr, stdout=self.stdout)

    def testRaw(self):
        """Test running valid code."""
        mark = "The test has passed."
        with self.ioPatcher():
            main.main(['P("%s")' % mark])
        self.assertEqual(mark, self.stdout.getvalue().strip())
        self.assertFalse(self.stderr.getvalue())

    def testHelp(self):
        with self.ioPatcher():
            self.assertRaises(SystemExit, main.main, ['-h'])

        self.assertIn(constants.DESCRIPTION, self.stdout.getvalue())
        self.assertFalse(self.stderr.getvalue())

    def testConflict(self):
        """Checks that line-mode and raw mode are incompatible."""
        with self.ioPatcher():
            self.assertRaises(SystemExit, main.main, ['-b', 'print(42)', 'print(43)'])

        self.assertFalse(self.stdout.getvalue())
        self.assertIn('lonely code snippet', self.stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
