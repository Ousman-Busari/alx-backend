#!/usr/bin/env python3
"""
MRU Cache
"""
BaseCaching = __import__("base_caching").BaseCaching


class MRUCache(BaseCaching):
    """MRU Cache policy"""
    def __init__(self):
        """Initializes a new MRU Cache"""
        self.list_of_recent_keys = []
        super().__init__()

    def put(self, key, item):
        """Add an item to the cache"""
        if key is None or item is None:
            return

        if len(self.cache_data) == BaseCaching.MAX_ITEMS:
            if key in self.cache_data:
                self.list_of_recent_keys.remove(key)
                # self.list_of_recent_keys.insert(-1, key)
            else:
                most_recent = self.list_of_recent_keys.pop()
                print("DISCARD:", most_recent)
                del self.cache_data[most_recent]
        self.cache_data[key] = item
        self.list_of_recent_keys.append(key)

    def get(self, key):
        """Get an item by key"""
        if key is not None and key in self.cache_data:
            self.list_of_recent_keys.remove(key)
            self.list_of_recent_keys.append(key)
        return self.cache_data.get(key)
