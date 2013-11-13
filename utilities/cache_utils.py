import re
import itertools
import functools
import hashlib

from django.conf import settings
from django.core.cache import cache
from django.template.defaultfilters import slugify


def cached(key, duration=None):
    """Wraps caching around an existing function, using the given key, duration, and
       call-time function arguments.
    
    Use like:
    
    @cached("work-for-x", 600)
    def work(*args, **kwargs):
        # do work here
        return result
    
    result = work(*args, **kwargs) # result will come from cache if possible
    """
    
    if not duration:
        duration = settings.CACHE_MIDDLEWARE_SECONDS
    
    def decorator(func):
        def inner(*args, **kwargs):
            key_bits = [settings.CACHE_MIDDLEWARE_KEY_PREFIX, key]
            [key_bits.append(slugify(str(val))) for val in args]
            [key_bits.append(str(val)) for val in kwargs.iteritems()]
            full_key = '|'.join(key_bits)
            result = cache.get(full_key)
            if not result:
                result = func(*args, **kwargs)
                cache.set(full_key, result, duration)
            return result
        inner.__name__ = "@cached %s" % func.__name__
        inner.__doc__ = "@cached. %s" % func.__doc__
        return inner
    return decorator


def cached_method(keyfunc, duration=None):
    """Wraps caching around an existing method, for a given duration,
       creating a key from the method name and call-time arguments.
    
    Use like:
    
    class MyClass:
        @cached(600)
        def my_method(self, *args, **kwargs):
            # do work here
            return result
    """

    if not duration:
        duration = settings.CACHE_MIDDLEWARE_SECONDS
    
    def decorator(func):
        def inner(obj, *args, **kwargs):
            key = keyfunc(obj, func.__name__, *args, **kwargs)
            result = cache.get(key)
            
            # hack in case the result has a dodgy __eq__ method (ie eventtools)
            if not result and result == None:
                result = func(obj, *args, **kwargs)
                cache.set(key, result, duration)
            return result
        inner.__name__ = func.__name__
        inner.__doc__ = func.__doc__
        return inner
    return decorator

def model_method_key(obj, func_name, *args, **kwargs):
    '''Creates a cache key for a cached model method using the 
       cached_method decorator.'''
        
    key = [settings.CACHE_MIDDLEWARE_KEY_PREFIX,
           func_name,
           obj._meta.app_label,
           obj._meta.module_name,
           obj.pk]
    for extra in (args, kwargs):
        if len(extra):
            key.append(hashlib.sha1(str(extra)).hexdigest()[:8])
    return '-'.join(key)

def manager_method_key(obj, func_name, *args, **kwargs):
    '''Creates a cache key for a cached manager method using the 
       cached_method decorator.'''
        
    key = [settings.CACHE_MIDDLEWARE_KEY_PREFIX,
           func_name,
           obj.model._meta.app_label,
           obj.model._meta.module_name,
           obj.__class__.__name__]
    
    for extra in (args, kwargs):
        if len(extra):
            key.append(hashlib.sha1(str(extra)).hexdigest()[:8])
    
    return '-'.join(key)

cached_model_method = functools.partial(cached_method, keyfunc=model_method_key)
cached_manager_method = functools.partial(cached_method, keyfunc=manager_method_key)



