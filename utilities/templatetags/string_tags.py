from django import template


register = template.Library()


# like the built in add, but for strings
@register.filter
def append(value, arg):
    return str(value) + str(arg)
append.is_safe = False

@register.filter
def prepend(value, arg):
    return str(arg) + str(value)
prepend.is_safe = False
