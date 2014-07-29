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

"""Tests for the tty module."""

import unittest

from py1 import template_reader
from py1 import tty


class TestColors(unittest.TestCase):

    def setUp(self):
        self.test_code = template_reader.build_code(
            ['c = 0'], ['c += 1'], ['P(c)'])

    def test_count_ansi_colors_terminfo(self):
        """Validates tty.count_ansi_colors while reading termingo ."""
        # This is not hardcoded and will cause a ncurse lookup.
        # Afterward ncurse will always return the value from its lookup :-(
        colors = tty.count_ansi_colors('screen-16color-s')
        # Accepts 0 as the test host might not have a valid terminfo setup.
        self.assertIn(colors, (0, 16))

    def test_count_ansi_colors_hardcoded(self):
        """Validates tty.count_ansi_colors with a few known-good."""
        for term_name, count in (
                ('xterm-256color', 256),
                ('xterm-16color', 16),
                ('xterm', 8),
                ('screen-256color', 256),
                ('screen-16color', 16),
                ('screen', 8),
                ('unknown', 0),
        ):
            self.assertEqual(count, tty.count_ansi_colors(term_name))

    def test_ansi_highlight_code_noop(self):
        """Checks that specifying colors results in ANSI code."""
        self.assertEqual(
            self.test_code,
            tty.ansi_highlight_code(
                self.test_code,
                ansi_colors=0))
        for colors in (8, 16, 256):
            self.assertIn(
                '\x1b',
                tty.ansi_highlight_code(
                    self.test_code,
                    ansi_colors=colors))


if __name__ == '__main__':
    unittest.main()
