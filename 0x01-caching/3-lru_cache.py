#!/usr/bin/env python3
"""
LRU cache
"""
BaseCaching = __import__("base_caching").BaseCaching


class LRUCache(BaseCaching):
    """LRU cache policies"""
    def __init__(self):
        """Initiliazes a new LIFO cache"""
        self.list_of_recent_keys = []
        super().__init__()

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return

        self.list_of_recent_keys.insert(0, key)
        if len(self.cache_data) == BaseCaching.MAX_ITEMS:
            least_recent = self.list_of_recent_keys[-1]
            if key not in self.cache_data:
                print("DISCARD:", least_recent)
            del self.cache_data[least_recent]
        self.cache_data[key] = item
        self.list_of_recent_keys = self.list_of_recent_keys[:4]

    def get(self, key):
        """Gets an item by key"""
        if key is not None and key in self.cache_data:
            self.list_of_recent_keys.remove(key)
            self.list_of_recent_keys.insert(0, key)
        return self.cache_data.get(key)
