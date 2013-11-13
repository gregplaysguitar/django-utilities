from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Create permissions for all INSTALLED_APPS"

    def handle_noargs(self, **options):
        from django.contrib.auth.management import create_permissions
        from django.db.models import get_apps
        for app in get_apps():
            create_permissions(app, None, 2)