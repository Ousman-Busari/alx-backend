#!/usr/bin/env python3
"""
FIFO Cache
"""
BaseCaching = __import__("base_caching").BaseCaching


class FIFOCache(BaseCaching):
    """
    A caching system with FIFO caching policies
    """
    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return
        if len(self.cache_data) == BaseCaching.MAX_ITEMS and (key not in
           self.cache_data):
            first_in = list(self.cache_data.keys())[0]
            print("DISCARD:", first_in)
            del self.cache_data[first_in]
        self.cache_data[key] = item

    def get(self, key):
        """Get an item in the cache by key"""
        return self.cache_data.get(key)
