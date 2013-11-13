import re

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings


holding_url = reverse(getattr(settings, 'HOLDING_PAGE_VIEW', 'admin:index'))
ALLOWED_REGEX = re.compile('^(?:%s|/media|/static|/admin)' % holding_url)

class StaffOnlyMiddleware:
    def process_request(self, request):
        if not request.user.is_staff and not ALLOWED_REGEX.match(request.path_info):
            return HttpResponseRedirect(holding_url)
