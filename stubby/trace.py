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

This module contains some tracing code to detect the flow of component
instantiation. The trace logs are made available on top of debug logging.

"""


__author__ = "Praveen Shirali <praveengshirali@gmail.com>"


from functools import wraps
from logging import getLogger


TRACE = False
log = getLogger(__name__)


def trace(msg):
    global TRACE
    if TRACE is True:
        log.info("{}{}{}".format('\x1b[31m', msg, '\x1b[m'))


def set_trace(boolean):
    global TRACE
    TRACE = boolean


def trace_method(cls):
    def outer(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            self_cls = self.__class__.__mro__[0]
            retval = func(self, *args, **kwargs)
            if cls is self_cls:
                trace("Assembled {}".format(self))
            return retval
        return inner
    return outer


def traceable(cls):
    init = getattr(cls, "__init__")
    setattr(cls, "__init__", trace_method(cls)(init))
    return cls
