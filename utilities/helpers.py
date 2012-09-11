from django.conf import settings
from django.core.cache import cache
import re
from django.template.defaultfilters import slugify
import itertools


class Indexable(object):    
    def __init__(self,it):
        self.it=it
        self.already_computed=[]
    def __iter__(self):
        for elt in self.it:
            self.already_computed.append(elt)
            yield elt
    def __getitem__(self,index):
        try:
            max_idx=index.stop
        except AttributeError:
            max_idx=index
        n=max_idx-len(self.already_computed)+1
        if n > 0:
            self.already_computed.extend(itertools.islice(self.it,n))
        return self.already_computed[index]   


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
            [key_bits.append(str(val)) for val in args]
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


def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator."""
    
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value
    

def form_errors_as_string(form):
    '''Render a django form's error list in plain text.'''
    
    if form.errors:
        errors = []
        
        if '__all__' in form.errors:
            errors.append(', '.join(form.errors['__all__']))
        for i in form.fields.keys():
            if i in form.errors:
                errors.append("%s: %s" % (form[i].label, ', '.join(form.errors[i])))
        
        return '\n'.join(errors)
    else:
        return None
