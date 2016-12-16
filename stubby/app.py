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

This module has the implementation for the Bottle HTTP server.

"""


__author__ = "Praveen Shirali <praveengshirali@gmail.com>"


import os
import sys
import logging
import bottle
import signal
import pprint

from .trace import traceable


log = logging.getLogger(__name__)
all_methods = ("GET", "POST", "PUT", "DELETE", "PATCH")


class SignalHandler(object):
    """A class which registers signals with handlers"""

    def __init__(self, sigstr, handler):
        self._sigstr = sigstr
        self._handler = handler
        try:
            self._handler_name = handler.func_name
        except:
            self._handler_name = handler
        signum = getattr(signal, sigstr)
        log.debug(
            "Registered signal {} --> '{}'".format(sigstr,
                                                   self._handler_name)
        )
        signal.signal(signum, self._handle_signal)

    def _handle_signal(self, signum, frame, *args, **kwargs):
        log.debug("Invoking handler for signal {}".format(self._sigstr))
        data = self._handler()
        if data:
            print("- " * 40)
            pprint.pprint(data)
            print("- " * 40)
        elif data is None:
            pass
        else:
            log.info("No data from signal handler '{}'.".format(
                self._handler_name))


@traceable
class Application(object):
    """This class represents the application with the webserver at its core"""

    def __init__(self, cfg, logger, stats_collector):
        """
        Args:
            cfg (stubby.contract.ConfigContract): The config instance
                from which to retrieve the hostname and port
            logger (stubby.contract.Logger): The logger to be used
            stats_collector (stubby.contract.StatsCollectorContract):
                The instance of the stats collector which must be used
                to store request stats.
        """
        self._config = cfg.get_config()
        self._logger = logger
        self._get_stats = stats_collector.get_stats
        self._reset_stats = stats_collector.reset_stats
        self._new_record = stats_collector.new_record
        self._srv = bottle.Bottle()
        self._opts = dict(host=self._config.address,
                          port=self._config.port,
                          quiet=True)
        self._help_info = {}

    def start_up(self):
        s = sys.version_info
        py_info = "Python {}.{}.{}".format(s.major, s.minor, s.micro)
        log.info("")
        log.info("     |         |    |         ")
        log.info(",---.|--- .   .|---.|---.,   .")
        log.info("`---.|    |   ||   ||   ||   |")
        log.info("`---'`---'`---'`---'`---'`---|")
        log.info("                         `---'")
        log.info("")
        log.info("pid = {} | {}".format(os.getpid(), py_info))

    def register_routes(self):
        if self._config.skip_ctrl is False:
            self._route("/_st/stats", ["GET"], self._get_stats,
                        desc="Show request statistics collected so far")
            self._route("/_st/reset", ["GET"], self._reset_stats,
                        desc="Reset current stats")
            self._route("/_st/help", ["GET"], self._show_help,
                        desc="Show this help.")
        else:
            log.info("*** Detected option `--skip-ctrl`.")
            log.info("    Skipped registering control routes.")
        self._route("/<url:re:.*>", all_methods, self._stub_handler,
                    meta="<URL>", desc="All request <URL>s are recorded")

    def run(self):
        self.start_up()
        SignalHandler("SIGUSR1", self._get_stats)
        SignalHandler("SIGUSR2", self._reset_stats)
        self.register_routes()
        try:
            log.info("Bottle {} web-server listening on http://{}:{}".format(
                bottle.__version__,
                self._config.address,
                self._config.port
            ))
            log.info("Press Ctrl+C to stop the server.")
            self._srv.run(**self._opts)
        except Exception as e:
            log.exception(e)
        finally:
            print("")
            log.info("Bye.")

    def _route(self, url, methods, handler, desc="", meta=None):
        self._srv.route(url, methods, handler)
        h_url = url if meta is None else meta
        h_key = "[{}] {}".format(",".join(methods), h_url)
        self._help_info[h_key] = desc
        log.debug("Registered route {}".format(h_key))

    def _stub_handler(self, url):
        path = bottle.request.path
        query = bottle.request.urlparts.query
        method = bottle.request.method
        if query:
            path = "{}?{}".format(path, query)
        self._new_record(method, path)

    def _show_help(self):
        return self._help_info
