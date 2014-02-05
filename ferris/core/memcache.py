# -*- coding: utf-8 -*-

from google.appengine.api import memcache
from functools import wraps
import inspect


none_sentinel_string = u'☃☸☃ - memcache none sentinel'


def _cache_invalidator(key):
    """ Generates a function that will invalidate the given cache key """
    def f():
        memcache.delete(key)
    return f


def _cache_getter(key):
    """ Generates a function that will get the cached data of a key """
    def f():
        data = memcache.get(key)
        if data == none_sentinel_string:
            return None
        return data
    return f


def cached(key, ttl=0):
    """
    Decorator that given a cache key and optionally a time to live will automatically
    cache the result of a function in memcache. The next time the function is called it
    will return the result from memcache (if it's still there). This decorator does not
    take arguments to the wrapped function into account- you can use cached_by_args for
    that.

    This function also adds the cached, uncached, and clear_cache functions to the
    wrapped function that allow you to get the cached and uncached values and clear the
    cache.
    """
    def wrapper(f):
        @wraps(f)
        def dispatcher(*args, **kwargs):
            data = memcache.get(key)

            if data == none_sentinel_string:
                return None

            if data is None:
                data = f(*args, **kwargs)
                memcache.set(key, none_sentinel_string if data is None else data, ttl)

            return data

        setattr(dispatcher, 'clear_cache', _cache_invalidator(key))
        setattr(dispatcher, 'cached', _cache_getter(key))
        setattr(dispatcher, 'uncached', f)
        return dispatcher
    return wrapper


def cached_by_args(key, ttl=0):
    """
    Similar to @cached, but takes arguments into account. It will turn each argument into
    a string an use it as part of the key. If the first argument is 'self' or 'cls', it will
    ignore it.
    """
    def wrapper(f):
        argspec = inspect.getargspec(f)[0]

        if len(argspec) and argspec[0] in ('self', 'cls'):
            is_method = True
        else:
            is_method = False

        @wraps(f)
        def dispatcher(*args, **kwargs):
            targs = args if not is_method else args[1:]
            arg_key = (key + ':' + _args_to_string(*targs, **kwargs))

            @cached(arg_key, ttl)
            def inner_dispatcher():
                return f(*args, **kwargs)

            return inner_dispatcher()
        return dispatcher
    return wrapper


def _args_to_string(*args, **kwargs):
    return ':'.join((','.join(map(str, args)),
        ','.join(map(str, kwargs.keys())),
        ','.join(map(str, kwargs.values()))))
