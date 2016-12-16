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

This module contains `contracts` for the various classes in the application.
The contract defines the interface (methods, properties etc) that the
actual class must implement. A class which derives from the contract raises
an exception on instantiation unless it implements the interface defined in
the contract.

Further reading:
https://en.wikipedia.org/wiki/Design_by_contract
https://docs.python.org/3/library/abc.html

"""


__author__ = "Praveen Shirali <praveengshirali@gmail.com>"


from six import with_metaclass
from abc import ABCMeta, abstractmethod, abstractproperty


class ConfigContract(with_metaclass(ABCMeta)):
    """
    This contract must be implemented by the service which manages the
    configuration for the application.
    """

    @abstractmethod
    def get_config(self):
        """
        Returns an instance who's attributes contain the config
        parameters.
        """


class StatsCollectorContract(with_metaclass(ABCMeta)):
    """
    This contract must be implemented by the class which manages stats
    for HTTP requests.
    """

    @abstractproperty
    def name(self):
        """Returns the name of the stats collector."""

    @abstractmethod
    def new_record(self, method, url):
        """
        Adds a new record into the stat collector.
        Args:
            method (str): The HTTP method supported by the stub server.
            url (str): The URL of the request.
        """

    @abstractmethod
    def reset_stats(self):
        """
        Resets all the stats
        """

    @abstractmethod
    def get_stats(self):
        """
        Returns the current stats in the following format:
        {
            "<http-method>": {
                <uri>: <count>,
                ...
            },
            ...
        }
        """
