# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

from crash.cache import CrashCache

class CrashCacheVM(CrashCache):
    def __init__(self) -> None:
        super().__init__()

    def refresh(self) -> None:
        pass

cache = CrashCacheVM()
