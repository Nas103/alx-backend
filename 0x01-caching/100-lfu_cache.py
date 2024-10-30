#!/usr/bin/python3
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.freq = {}
        self.usage = {}
        self.min_freq = 0

    def put(self, key, item):
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self._update_freq(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                self._evict()
            self.cache_data[key] = item
            self.freq[key] = 1
            self.usage[key] = len(self.cache_data)
            self.min_freq = 1

    def get(self, key):
        if key is None or key not in self.cache_data:
            return None
        self._update_freq(key)
        return self.cache_data[key]

    def _update_freq(self, key):
        freq = self.freq[key]
        self.freq[key] += 1
        if (freq == self.min_freq and
                not any(f == self.min_freq for f in self.freq.values())):
            self.min_freq += 1

    def _evict(self):
        lfu_keys = [k for k, f in self.freq.items() if f == self.min_freq]
        if len(lfu_keys) > 1:
            lru_key = min(lfu_keys, key=lambda k: self.usage[k])
        else:
            lru_key = lfu_keys[0]
        print(f"DISCARD: {lru_key}")
        del self.cache_data[lru_key]
        del self.freq[lru_key]
        del self.usage[lru_key]
