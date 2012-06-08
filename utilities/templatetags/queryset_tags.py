from django import template
from django.db import models


register = template.Library()



@register.filter
def exclude(qs, exclude):
    if isinstance(exclude, models.query.QuerySet):
        return qs.exclude(pk__in=exclude.values_list('pk', flat=True))
    elif isinstance(exclude, models.Model):
        return qs.exclude(pk=exclude.pk)        
    elif exclude:
        # assume it's an integer primary key
        return qs.exclude(pk=exclude)
    else:
        return qs
