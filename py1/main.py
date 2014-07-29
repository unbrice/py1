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

import argparse
import sys

from py1 import template_reader
from py1 import constants
from py1 import curly
from py1 import runner
from py1 import tty


def _get_option_parser():
    p = argparse.ArgumentParser(
        description=constants.LONG_DESCRIPTION,
        prog=constants.NAME,
    )
    p.set_defaults(
        dump_code=False,
    )
    p.add_argument('-c', '--dump-code', action='store_true')
    p.add_argument('-V', '--version', action='version',
                   version='%%(prog)s %s' % constants.VERSION)
    p.add_argument('-b', '--begin', action='append', default=[])
    p.add_argument('-e', '--end', action='append', default=[])
    p.add_argument('-l', '--each-line', action='append', default=[])
    p.add_argument('python_one_liner', nargs='?')
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
    if args.python_one_liner:
        # We expect no options if given a one liner.
        for opt in ('begin', 'end', 'each_line'):
            if getattr(args, opt):
                snippet = _abreviate(args.python_one_liner)
                parser.error(
                    '--%s is specified yet there is a lonely code snippet, try'
                    ' fixing quotes or adding --begin/-b before: "%s"' %
                    (opt, snippet))
        begin = [args.python_one_liner]
    else:
        begin = args.begin

    code = template_reader.build_code(
        begin=_uncurl_list_or_die(begin),
        each_line=_uncurl_list_or_die(args.each_line),
        end=_uncurl_list_or_die(args.end),
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
        print('You can see the unescaped code with --dump_code',
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())


# echo 42foo43 | python3 -m main -b 'WRE="foo"' -l "P(W[0], int(W[1]) * 42)"
# echo 42 vs 43 | python3 -m main -l "vals=M('(\d+) vs (\d+)', L)"  -l
# 'P(int(vals[1]) + 1 == int(vals[2]))' -c
