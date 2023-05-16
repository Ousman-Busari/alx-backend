#!/usr/bin/env pythom3
"""
LIFO Cache
"""
BaseCaching = __import__("base_caching").BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFO caching Policy
    """
    def put(self, key, item):
        """ Adds  an item in the cache"""
        if key is None or item is None:
            return
        if len(self.cache_data) == BaseCaching.MAX_ITEMS:
            if key in self.cache_data:
                del self.cache_data[key]
                self.cache_data[key] = item
                return
            last_in = list(self.cache_data.keys())[-1]
            del self.cache_data[last_in]
            print("DISCARD:", last_in)
        self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        return self.cache_data.get(key)
