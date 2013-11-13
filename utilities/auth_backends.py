from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

class EmailBackend(object):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            #print kwargs, user
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False
