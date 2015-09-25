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

import argparse
import sys

from py1 import template_reader
from py1 import constants
from py1 import curly
from py1 import imports
from py1 import runner
from py1 import tty


_ARG_CONCISE = 'concise'
_ARG_FULL = 'full'

def _get_option_parser():
    p = argparse.ArgumentParser(
        description=constants.LONG_DESCRIPTION,
        prog=constants.NAME,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=constants.EPILOG,
    )
    p.set_defaults(
        dump_code=False,
    )
    p.add_argument('-b', '--begin', action='append', default=[],
                   metavar='PY', help='Code run once first.')
    p.add_argument('-l', '--each-line', action='append', default=[],
                   metavar='PY', help='Code run each line.')
    p.add_argument('-e', '--end', action='append', default=[],
                   metavar='PY', help='Code run once at the end.')
    p.add_argument('-i', '--import', action='append', default=[],
                   dest='import_list', metavar='IMPORT',
                   help='Imports modules described in abbreviated form.')
    p.add_argument('-c', '--dump-code', '--code',
                   default=False,  # Value if not provided
                   const=_ARG_CONCISE,  # Value if provided without argument
                   nargs='?', choices=[_ARG_CONCISE, _ARG_FULL],
                   help='Show the code instead of executing it.')
    p.add_argument('-V', '--version', action='version',
                   version='%%(prog)s %s' % constants.VERSION)
    p.add_argument('single_snippet', nargs='?', metavar='single_snippet')
    return p


def _abreviate(s):
    if len(s) < 10:
        return s
    else:
        return '%s...%s' % (s[:3], s[-3:])


def _uncurl_list_or_die(escaped_list):
    result = []
    for escaped in escaped_list:
        try:
            result.append(curly.unescape(escaped))
        except curly.Error as e:
            snippet = _abreviate(escaped)
            print('Invalid program: "%s": %s' % (snippet, e), file=sys.stderr)
            sys.exit(1)
    return result


def main(args=None):
    parser = _get_option_parser()
    args = parser.parse_args(args)

    begin = [imports.expand_short(i) for i in args.import_list]

    if args.single_snippet:
        # We expect no additional code if given a single snippet.
        for opt in ('begin', 'end', 'each_line'):
            if getattr(args, opt):
                snippet = _abreviate(args.single_snippet)
                parser.error(
                    '--%s is specified yet there is a lonely code snippet, try'
                    ' fixing quotes or adding --begin/-b before: "%s"' %
                    (opt, snippet))
        begin.append(args.single_snippet)
    else:
        begin += args.begin

    code = template_reader.build_code(
        begin=_uncurl_list_or_die(begin),
        each_line=_uncurl_list_or_die(args.each_line),
        end=_uncurl_list_or_die(args.end),
        concise=args.dump_code == _ARG_CONCISE,
    )

    if args.dump_code:
        if sys.stdout.isatty():
            try:
                colors = tty.count_ansi_colors()
                code = tty.ansi_highlight_code(code, colors)
            except:
                pass  # Never fail on highlighting.
        print(code)
        return 0

    code_globals = runner.build_globals()
    try:
        runner.run(code, code_globals)
    except runner.RunFailed as e:
        print('Running the one-liner failed:', file=sys.stderr)
        print(e.message, file=sys.stderr)
        print('You can see the unescaped code with --code=full',
              file=sys.stderr)
        sys.exit(1)

