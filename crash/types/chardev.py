# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import gdb
import sys

from crash.infra import CrashBaseClass, export
from crash.util import array_size

if sys.version_info.major >= 3:
    long = int

class ChardevClass(CrashBaseClass):
    __types__ = [ 'struct device' ]
    __symvals__ = [ 'chrdevs' ]
    __symbol_callbacks__ = [ ('chrdevs', 'chrdevs_callback') ]

    count = None

    @classmethod
    def chrdevs_callback(cls, symbol):
        cls.count = array_size(cls.chrdevs)

    @export
    def for_each_chardev(self):
        # TODO crash lists other devices, perhaps from cdev_map and following
        # next pointers
        for i in range(self.count):
            if long(self.chrdevs[i]):
                yield self.chrdevs[i]
