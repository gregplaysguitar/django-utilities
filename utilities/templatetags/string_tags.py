from django import template


register = template.Library()


# like the built in add, but for strings
@register.filter
def append(value, arg):
    return unicode(value) + unicode(arg)
append.is_safe = False

@register.filter
def prepend(value, arg):
    return unicode(arg) + unicode(value)
prepend.is_safe = False
