from django import forms
from django.template import Library


register = Library()


@register.filter()
def widgettype(widget):
    if isinstance(widget, forms.CheckboxInput):
        return 'checkbox'
    elif isinstance(widget, forms.RadioSelect):
        return 'radio'
    elif isinstance(widget, forms.Textarea):
        return 'textarea'
    elif isinstance(widget, forms.Select):
        return 'select'
    elif isinstance(widget, forms.TextInput):
        return 'text'
        
