#!/usr/bin/python3
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

from crash.cache import CrashCache

class CrashCacheSlab(CrashCache):

    def __init__(self):
        super().__init__()
        self.populated = False
        self.kmem_caches = dict()
        self.kmem_caches_by_addr = dict()

    def refresh(self):
        self.populated = False
        self.kmem_caches = dict()
        self.kmem_caches_by_addr = dict()

cache = CrashCacheSlab()
