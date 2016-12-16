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

This module caters to the logging nees of the application. There are three
loggers to choose from (mainly to demonstrate configuration through Aglyph).

"""


__author__ = "Praveen Shirali <praveengshirali@gmail.com>"


import logging
from .trace import traceable
log = logging.getLogger(__name__)


@traceable
class Logger(object):
    """A logger which does nothing"""

    def __init__(self, *args, **kwargs):
        pass


@traceable
class BasicLogger(Logger):
    """Implementation for a basic console logger."""

    def __init__(self, cfg):
        self._config = cfg.get_config()
        self._logger = logging.getLogger("stubby")
        self._sh = logging.StreamHandler()
        self._logger.addHandler(self._sh)
        level = "DEBUG" if self._config.debug is True else "INFO"
        self._logger.setLevel(level)
        if self._config.aglyph is True:
            self._aglyph = logging.getLogger("aglyph")
            self._aglyph.setLevel(level)
            self._aglyph.addHandler(self._sh)


@traceable
class ColorLogger(BasicLogger):
    """A colorful, well formatted console logger."""

    def __init__(self, cfg):
        super(ColorLogger, self).__init__(cfg)
        from colorlog import ColoredFormatter
        formatter = ColoredFormatter(
            "%(asctime)s.%(msecs)03d %(log_color)s%(levelname)10s%(reset)s "
            "| %(message_log_color)s%(message)s",
            datefmt="%Y-%M-%d %H:%m:%S",
            reset=True,
            log_colors={
                "DEBUG":    "bold_cyan",
                "INFO":     "bold_green",
                "WARNING":  "bold_yellow",
                "ERROR":    "bold_red",
                "CRITICAL": "bold_red,bg_white",
            },
            secondary_log_colors={
                "message": {
                    "DEBUG":    "cyan",
                    "INFO":     "green",
                    "WARNING":  "yellow",
                    "ERROR":    "red",
                    "CRITICAL": "red,bg_white",
                }
            },
            style="%"
        )
        self._sh.setFormatter(formatter)
