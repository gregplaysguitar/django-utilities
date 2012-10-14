from django import forms
from django.conf import settings
from django.core.mail import EmailMessage

from django.template import loader, Context
from django.contrib.sites.models import Site


class BaseContactForm(forms.Form):
    recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]
    subject_extra = ""
    template_name = 'contact_form/generic_form.txt'


    def from_email(self):
        if 'email_address' in self.cleaned_data:
            return self.cleaned_data['email_address']
        if 'email' in self:
            return self.cleaned_data['email']
        else:
            return settings.DEFAULT_FROM_EMAIL


    def message(self):
        return loader.render_to_string(self.template_name, self.get_context())


    def get_context(self):
        form_data = []
        for field in self.cleaned_data:
            item = {
                'label': self[field].label,
                'value': self.cleaned_data[field],
            }
            if isinstance(self[field].field.widget, forms.Textarea):
                item['long'] = True
            form_data.append(item)

        return Context({
            'form_data': form_data,
            'site': Site.objects.get_current(),
        })


    def send(self):
        message = EmailMessage(
            "%s %s" % (settings.EMAIL_SUBJECT_PREFIX, self.subject_extra),
            self.message(),
            self.from_email(),
            self.recipient_list,
        )

        message.send()




