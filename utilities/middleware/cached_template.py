from django.template import Template
from django.template.context import RequestContext

class CachedTemplateMiddleware(object):    
    def process_response(self, request, response):
        '''Re-render response content, to catch anything that was excluded via the
           `{% raw %}` templatetag.
           This must appear before `'django.middleware.cache.UpdateCacheMiddleware'`
           in your `MIDDLEWARE_CLASSES` setting. '''
           
        if request.method == 'GET' and response['content-type'].startswith('text/html'):
            t = Template(response.content)
            response.content = t.render(RequestContext(request))
        return response