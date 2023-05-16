#!/usr/bin/env python3
"""
Basic cache
"""
BaseCaching = __import__("base_caching").BaseCaching


class BasicCache(BaseCaching):
    """
    Basic Cache implementation
    """
    def put(self, key, item):
        """Stores a new item into the cache with a key"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """Get the item value of a key in the cache"""
        return self.cache_data.get(key)
