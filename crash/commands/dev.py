# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys

if sys.version_info.major >= 3:
    long = int

from crash.commands import CrashCommand, CrashCommandParser
from crash.types.chardev import for_each_chardev

class DevCommand(CrashCommand):
    """display character and block devices

NAME
  dev - display character and block devices
"""
    def __init__(self, name):
        parser = CrashCommandParser(prog=name)

        parser.format_usage = lambda : "dev\n"
        super(DevCommand, self).__init__(name, parser)

    def execute(self, args):
        self._list_chardevs()
        # TODO self._list_block_dev()

    def _list_chardevs(self):
        print("{:^10} {:^16} {:^16} {:^16}"
            .format("CHRDEV", "NAME", "CDEV", "OPERATIONS"))

        for chardev in for_each_chardev():
            self.show_one_chardev(chardev)

    def show_one_chardev(self, chardev):
        # TODO print symbolic name of ops
        if long(chardev['cdev']):
            print("{:>10d} {:<16} {:016x} {:<16}"
                .format(int(chardev['major']), chardev['name'].string(),
                    long(chardev['cdev']), long(chardev['cdev']['ops'])))
        else:
            # TODO 
            # search for kobj_map.probes[major] array entry, "data" member
            # points to cdev
            print("{:>10d} {:<16} {:^16}"
                .format(int(chardev['major']), chardev['name'].string(),
                    '(none)'))


DevCommand("dev")
