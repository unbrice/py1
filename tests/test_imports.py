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

"""Tests for the imports module."""

import threading
import unittest

from py1 import imports


class TestExpand(unittest.TestCase):

    def testGoodSamples(self):
        samples = [
            # The full syntax
            ('m1.m2.m3/i1:n1,i2:n2,i3', 'from m1.m2.m3 import i1 as n1,i2 as n2,i3'),
            # No from
            ('i1:n1,i2:n2,i3', 'import i1 as n1,i2 as n2,i3'),
            # Just one import
            ('i', 'import i'),
            # Import *
            ('i/*', 'from i import *'),
        ]

        for short_import, expanded_import in samples:
            self.assertEqual(expanded_import, imports.expand_short(short_import))

    def testInvalidSamples(self):
        samples = [
            # Extra "!"
            'i!',
            # Import star without scope
            '*',
            # Missing name
            'a:',
            # Missing module
            ':b',
        ]

        for short_import in samples:
            self.assertRaises(imports.BadShortSyntaxError, imports.expand_short, short_import)


if __name__ == '__main__':
    unittest.main()
