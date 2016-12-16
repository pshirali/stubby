#!/usr/bin/env python

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


Stubby is a (short and thick) HTTP stub server.
Refer to the README for more info.

This application utilizes Aglyph Dependency Injection framework,
and is meant to serve as a beginner's tutorial on how DI could be
used in Python. This application is not part of the official
documentation for Aglyph, nor does it cover all features that
Aglyph has to offer.


You are highly encouraged to explore more from the URLs below:
-------------------------------------------------------------
Repo: https://github.com/mzipay/Aglyph
Docs: http://aglyph.readthedocs.io/en/latest/


General DI reference:
-------------------------------------------------------------
http://www.aleax.it/yt_pydi.pdf
http://martinfowler.com/articles/injection.html
https://en.wikipedia.org/wiki/Dependency_injection


"""

__author__ = "Praveen Shirali <praveengshirali@gmail.com>"


if __name__ == "__main__":

    from aglyph.context import XMLContext
    from aglyph.assembler import Assembler

    context = XMLContext("app-context.xml")
    assembler = Assembler(context)

    # The CLIParser has been explicitly assembled to only address the
    # scenario of `-h/--help` being passed. This switch causes the parser
    # to show the help and quit. Aglyph catches the SystemExit exception
    # and prints a traceback. By explicitly assembling `st-config`, we
    # allow for SystemExit to not break the assembly of a class which
    # depended on it. Also, `st-config` is a singleton, and the parsed
    # args are cached for subsequent retrieval.
    #
    assembler.assemble("st-config").get_config()

    assembler.assemble("st-app").run()
