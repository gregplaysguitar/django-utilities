from django import template

register = template.Library()




@register.filter
def multiply(value, arg):
    return int(arg) * int(value)
multiply.is_safe = False
