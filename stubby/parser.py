# -*- coding: UTF-8 -*-

# Copyright (c) 2016 Praveen Shirali <praveengshirali@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from __future__ import unicode_literals, print_function


"""

This module contains the CLI parser for the application. This currently
serves as the only source of configuration for the application. Hence,
the CLI parser implements the ConfigContract.

"""


__author__ = "Praveen Shirali <praveengshirali@gmail.com>"


import sys
import argparse
from .trace import set_trace
from .contract import ConfigContract


class CLIParser(ConfigContract):
    """The command line parser."""

    def __init__(self, prog, description="", epilog=""):
        """
        Args:
            prog (str):
                The name of the script that launches the application
            description (str):
                The description of the application
            epilog (str):
                The text which appears as a footer in the CLI help.
        """
        self._config = None
        hr = "- " * 39
        if description:
            description = "{}\n{}".format(hr, description)
        if epilog:
            epilog = "{}\n{}".format(hr, epilog)

        self._parser = argparse.ArgumentParser(
            prog=prog, description=description, epilog=epilog,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        self._parser.add_argument(
            "-a", "--address", default="localhost",
            help="The address on which the HTTP server must listen."
        )
        self._parser.add_argument(
            "-p", "--port", type=int, default=8080,
            help="Port for the HTTP server."
        )
        self._parser.add_argument(
            "-d", "--debug", action="store_true", default=False,
            help="Enable debug logging on the application."
        )
        self._parser.add_argument(
            "-x", "--skip-ctrl", action="store_true", default=False,
            help=("If True, the app-routes with `/_st/*` are not "
                  "registered allowing the server to stub any URL. "
                  "Stats can still be retrieved and reset using "
                  "signals SIGUSR1 and SIGUSR2 respectively.")
        )
        self._parser.add_argument(
            "-t", "--trace", action="store_true", default=False,
            help="Trace object assembly execution."
        )
        self._parser.add_argument(
            "--aglyph", action="store_true", default=False,
            help="Enable logging on Aglyph library."
        )

    def _parse(self, args=None):
        if not args:
            args = sys.argv[1:]
        return self._parser.parse_args(args)

    def get_config(self):
        """
        Returns the parsed config as a namespace. The resolved config is
        cached and returned on subsequent requests.

        Returns:
            argparse.Namespace
        """
        if not self._config:
            self._config = self._parse()
            set_trace(self._config.trace)
        return self._config
