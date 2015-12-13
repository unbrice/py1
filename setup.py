#!/usr/bin/env python3
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

from distutils.command import build as upstream_build
from setuptools.command import install as upstream_install
import setuptools
from sphinx import setup_command as sphinx_command

from py1 import constants


class build(upstream_build.build):
    """Builds man pages and spinx doc as well."""

    sub_commands = upstream_build.build.sub_commands + [
        ('build_man', None),
        ('build_sphinx', None),
    ]


class install(upstream_install.install):
    """Builds man pages and spinx doc before to install."""

    def run(self):
        self.run_command('build_man')
        self.run_command('build_sphinx')
        super().run()


setuptools.setup(
    name=constants.NAME + 'cmd',
    version=constants.VERSION,

    description=constants.DESCRIPTION,
    long_description=constants.LONG_DESCRIPTION,


    author='Brice Arnould',
    author_email='unbrice@vleu.net',
    url='http://py1.vleu.net/',

    license='MIT',

    py_modules=[
        'py1.constants',
        'py1.curly',
        'py1.imports',
        'py1.main',
        'py1.runner',
    ],

    # The manpage is build by an alias of build_sphinx
    data_files=[('share/man/man1', ['build/sphinx/man/py1.1'])],
    cmdclass={
        'build_man': sphinx_command.BuildDoc,
        # Setups our build and install command that also builds the doc.
        'build': build,
        'install': install,
    },
    command_options={
        'build_man': {
            'builder': ('setup.py', 'man'),
        },
    },

    test_suite='tests',

    install_requires=[
        'pygments>=0.10',
    ],

    keywords='scripting awk one-liner oneliner',

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',

        # Audience
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        # Topics
        'Topic :: Software Development :: Interpreters',
        'Topic :: System :: Shells',
        'Topic :: Text Processing :: Filters',

        # Environment
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    packages=['py1'],

    entry_points={
        'console_scripts': [
            'py1 = py1.main:main',
        ],
    },
)
