from django import template
from utilities.easy_tag import easy_tag



register = template.Library()



class RangeNode(template.Node):
    def __init__(self, start, end, alias):
        self.start = start
        self.end = end
        self.alias = alias
        
    def render(self, context):
        start = template.Variable(self.start).resolve(context)
        end = template.Variable(self.end).resolve(context)
        if self.alias:
            context[self.alias] = range(start, end)
            return ''
        else:
            return range(start, end)

@register.tag
@easy_tag
def get_range(_tag, *args):
    if args[-2] == 'as':
        alias = args[-1]
        args = args[:-2]
    
    if len(args) == 1:
        start = '0'
        end = args[0]
    elif len(args) == 2:
        start, end = args
    else:
        raise template.TemplateSyntaxError('Bad arguments for get_range tag')

    return RangeNode(start, end, alias)



