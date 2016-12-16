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

This module has the implementation for the various stats collectors.

"""


__author__ = "Praveen Shirali <praveengshirali@gmail.com>"


import logging
import threading
import collections

from .contract import StatsCollectorContract
from .trace import traceable


log = logging.getLogger(__name__)


@traceable
class StatsCollector(StatsCollectorContract):
    """
    The StatsCollector manages multiple collectors at once. It shares the
    same API as it obeys a common contract. When a call is made to it,
    it simply calls individual collectors by the same method name,
    collates the result from each collector and returns.
    """

    def __init__(self, name, *collectors):
        super(StatsCollector, self).__init__()
        self._collectors = collectors
        self._lock = threading.Lock()

    @property
    def name(self):
        return self._name

    def _call(self, member, *args):
        result = {}
        for c in self._collectors:
            with self._lock:
                try:
                    member_obj = getattr(c, member)
                    result[c.name] = member_obj(*args)
                except Exception as e:
                    log.exception(e)
        args_msg = " ".join(["{}".format(a) for a in args])
        suffix = " with args {}".format(args_msg) if len(args) else ""
        log.debug("Method '{}' called{}".format(member, suffix))
        return result

    def new_record(self, method, url):
        self._call("new_record", method, url)

    def reset_stats(self):
        self._call("reset_stats")

    def get_stats(self):
        return self._call("get_stats")


@traceable
class BaseCollector(StatsCollectorContract):

    def __init__(self, name):
        super(BaseCollector, self).__init__()
        self._name = name

    @property
    def name(self):
        return self._name


@traceable
class URLHitCollector(BaseCollector):

    def __init__(self, name):
        super(URLHitCollector, self).__init__(name)
        self._collector = dict()

    def new_record(self, method, url):
        if method not in self._collector:
            self._collector[method] = collections.Counter()
        self._collector[method].update([url])

    def reset_stats(self):
        self._collector.clear()

    def get_stats(self):
        return {k: dict(v) for k, v in self._collector.items()}


@traceable
class MethodHitCollector(BaseCollector):

    def __init__(self, name):
        super(MethodHitCollector, self).__init__(name)
        self._collector = collections.Counter()

    def new_record(self, method, url):
        self._collector.update([method])

    def reset_stats(self):
        self._collector.clear()

    def get_stats(self):
        return dict(self._collector)


@traceable
class WordHitCollector(BaseCollector):

    def __init__(self, name):
        super(WordHitCollector, self).__init__(name)
        self._collector = collections.Counter()

    def new_record(self, method, url):
        q = url.find("?")
        path = url[:q] if q >= 0 else url
        path = [s.strip() for s in path.split("/") if s.strip()]
        self._collector.update(path)

    def reset_stats(self):
        self._collector.clear()

    def get_stats(self):
        return dict(self._collector)
