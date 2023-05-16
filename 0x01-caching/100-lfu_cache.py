#!/usr/bin/env python3
"""
LFU Cache
"""
BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    """Instance of a least frequently used cache"""
    def __init__(self):
        """Initializes a new instance of LFU cache"""
        self.keys_counts = {}
        # self.recent_keys = []
        super().__init__()

    def put(self, key, item):
        """Adds an item to the cache"""
        if key is None or item is None:
            return

        if len(self.cache_data) == BaseCaching.MAX_ITEMS:
            least_freq = min(list(self.keys_counts.values()))
            least_key = ""
            for k, v in self.keys_counts.items():
                if v == least_freq:
                    least_key = k
                    break

            if key in self.cache_data:
                self.cache_data[key] = item
                init_count = self.keys_counts[key]
                del self.keys_counts[key]
                self.keys_counts[key] = init_count + 1
                return
            if key not in self.cache_data:
                print("DISCARD:", least_key)
            del self.keys_counts[least_key]
            del self.cache_data[least_key]

        if key in self.keys_counts:
            init_count = self.keys_counts[key]
            del self.keys_counts[key]
            self.keys_counts[key] = init_count + 1
        else:
            self.keys_counts[key] = 1
        self.cache_data[key] = item

    def get(self, key):
        """Gets an item by key"""
        if key in self.keys_counts:
            init_count = self.keys_counts[key]
            del self.keys_counts[key]
            self.keys_counts[key] = init_count + 1
        return self.cache_data.get(key)
