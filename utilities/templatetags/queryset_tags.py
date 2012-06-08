from django import template


register = template.Library()



@register.filter
def exclude(qs, obj):
    return qs.exclude(pk=obj.pk)
