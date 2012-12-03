from django import template
from utilities.easy_tag import easy_tag


register = template.Library()


class AppendGetNode(template.Node):
    def __init__(self, path, dict):
        self.path = path
        self.dict = dict
                    
    def render(self, context):
        get = context['request'].GET.copy()

        for key in self.dict:
            if key != 'parser':
                val = template.Variable(self.dict[key]).resolve(context)
                if val:
                    get[key] = val
                elif key in get:
                    del get[key]
                            

        if self.path:
            path = template.Variable(self.path).resolve(context)
        else:
            path = context['request'].META['PATH_INFO']
                
        if len(get):
            path += '?%s' % get.urlencode()
        
        return path

@register.tag()
@easy_tag
def append_to_get(_tag_name, path=None, **dict):
    return AppendGetNode(path, dict)
