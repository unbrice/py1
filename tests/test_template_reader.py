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

"""Tests for the template_reader module."""

import uuid
import unittest

from py1 import template_reader
from py1.template_reader import build_code


class SanityChecks(unittest.TestCase):
    """Checks generated code has some properties."""
    
    def testHasReturns(self):
        """Ensure concise code does not contain full function body."""
        concise = build_code([], [], [], concise=True)
        full = build_code([], [], [], concise=False)
        self.assertNotIn('return', concise)
        self.assertIn('return', full)

    def testHasForLoop(self):
        """Ensure there is no for loop if there is no each_line code."""
        no_foreach = build_code(['x=1'], [], ['x=3'], concise=False)
        foreach = build_code(['x=1'], ['x=2'], ['x=3'], concise=False)
        self.assertNotIn('for', no_foreach)
        self.assertIn('for', foreach)

    def testHasCode(self):
        """Ensure the generated code contains the user code."""
        begin = 'begin = %s' % uuid.uuid4()
        for_each = 'for_each = %s' % uuid.uuid4()
        end = 'end = %s' % uuid.uuid4()
        generated = build_code([begin], [for_each], [end], concise=True)
        for code in [begin, for_each, end]:
            self.assertIn(code, generated)


if __name__ == '__main__':
    unittest.main()
