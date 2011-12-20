from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from django.forms.models import inlineformset_factory



def upgrade_user_admin(UserProfile=None, unique_email=False):
            
    class MyUserAdmin(UserAdmin):
        inlines = []
        actions = ['make_active', 'make_inactive',]
        list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login',]
        list_display = ['first_name', 'last_name', 'email', 'username', 'date_joined',]
        list_display_links = ['first_name', 'last_name', 'email', 'username']
        
        def make_active(self, request, queryset):
            rows_updated = queryset.update(is_active=True)
            if rows_updated == 1:
                message_bit = "1 person was"
            else:
                message_bit = "%s people were" % rows_updated
            self.message_user(request, "%s successfully made active." % message_bit)
    
        def make_inactive(self, request, queryset):
            rows_updated = queryset.update(is_active=False)
            if rows_updated == 1:
                message_bit = "1 person was"
            else:
                message_bit = "%s people were" % rows_updated
            self.message_user(request, "%s successfully made inactive." % message_bit)
    
    if unique_email:
        class MyUserForm(UserAdmin.form):
            class Meta:
                model = User
            
            def clean_email(self):
                email = self.cleaned_data['email']
                if email and User.objects.filter(email=email).exclude(pk=self.instance and self.instance.pk).count():
                    raise forms.ValidationError('That email address is already in use')
                else:
                    return email
        MyUserAdmin.form = MyUserForm

        
    if UserProfile:
        class UserProfileFormSet(inlineformset_factory(User, UserProfile)):
            def __init__(self, *args, **kwargs):
                super(UserProfileFormSet, self).__init__(*args, **kwargs)
                self.can_delete = False
        
        # Allow user profiles to be edited inline with User
        class UserProfileInline(admin.StackedInline):
            model = UserProfile
            fk_name = 'user'
            max_num = 1
            extra = 0
            formset = UserProfileFormSet
        MyUserAdmin.inlines += [UserProfileInline, ]

    # Re-register UserAdmin
    admin.site.unregister(User)
    admin.site.register(User, MyUserAdmin)

