"""
Cache module
"""

import time


class Cache(object):
    """Class that caches the Vercel API responses"""

    _cache_ = {}
    VALUE = 0
    EXPIRES = 1

    def __init(self):
        pass

    @classmethod
    def get(cls, key):
        """Get the value from the cache stored with 'key' if it exists"""
        try:
            if cls._cache_[key][cls.EXPIRES] > time.time():
                return cls._cache_[key][cls.VALUE]

            del cls._cache_[key]  # Delete the item if it has expired
            return None
        except KeyError:
            return None

    @classmethod
    def set(cls, key, value, duration=3600):
        """Store/overwite a value in the cache with 'key' and an optional duration (seconds)"""
        try:
            expires = time.time() + duration
        except TypeError:
            raise TypeError("Duration must be numeric")

        cls._cache_[key] = (value, expires)
        return cls.get(key)

    @classmethod
    def clean(cls):
        """Remove all expired items from the cache"""
        for key, _ in cls._cache_.items():
            # Attempting to fetch an expired item deletes it
            cls.get(key)

    @classmethod
    def purge(cls):
        """Remove all items from the cache"""
        cls._cache_ = {}
