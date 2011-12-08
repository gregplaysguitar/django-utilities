import copy

from django import template
from django import forms
from django.utils.datastructures import SortedDict

register = template.Library()

@register.tag
def get_fieldset(parser, token):
    try:
        name, fields, _from, form, _as, variable_name = token.split_contents()
        if _as != 'as':
            name, fields, _as, variable_name, _from, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('bad arguments for %r'  % token.split_contents()[0])

    return FieldSetNode(fields.split(','), variable_name, form)



@register.tag
def get_fieldset_excluding(parser, token):
    try:
        name, fields, _from, form, _as, variable_name = token.split_contents()
        if _as != 'as':
            name, fields, _as, variable_name, _from, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('bad arguments for %r'  % token.split_contents()[0])

    return FieldSetNode(fields.split(','), variable_name, form, True)







class FieldSetNode(template.Node):
    def __init__(self, fields, variable_name, form_variable, exclude_fields=False):
        self.fields = fields
        self.variable_name = variable_name
        self.form_variable = form_variable
        self.exclude_fields = exclude_fields

    def render(self, context):
        
        form = template.Variable(self.form_variable).resolve(context)
        new_form = copy.copy(form)
        
        # if any item in the fields is a form, add all the fields 
        # from that form to the list
        fields = []
        for f in self.fields:
            val = template.Variable(f).resolve(context)
            if getattr(val, 'fields', False):
                # assume it's a form
                for field in val.fields:
                    fields.append(field)
            else:
                # assume it's the field name as a string
                fields.append(val)
    
        if self.exclude_fields:
            new_form.fields = SortedDict([(key, value) for key, value in form.fields.items() if key not in fields])
        else:
            new_fields = []
            for key in fields:
                new_fields.append((key, form.fields[key]))
            new_form.fields = SortedDict(new_fields)

        context[self.variable_name] = new_form

        return u''

