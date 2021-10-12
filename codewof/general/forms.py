"""Forms for general website pages."""

from django import forms
from django.conf import settings
from django.core.mail import send_mail, mail_managers
from django.template.loader import render_to_string
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

MESSAGE_TEMPLATE = "{}\n\n-----\nMessage sent from {} <{}>\n"


class ContactForm(forms.Form):
    """Form for contacting website owners."""

    name = forms.CharField(required=True, label='Your name', max_length=100)
    from_email = forms.EmailField(required=True, label='Email to contact you')
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    cc_sender = forms.BooleanField(required=False, label='Send a copy to yourself')
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def send_email(self):
        """Send email if form is valid."""
        name = self.cleaned_data['name']
        subject = self.cleaned_data['subject']
        from_email = self.cleaned_data['from_email']
        message = self.cleaned_data['message']
        mail_managers(
            subject,
            MESSAGE_TEMPLATE.format(message, name, from_email),
        )
        if self.cleaned_data.get('cc_sender'):
            send_mail(
                subject,
                MESSAGE_TEMPLATE.format(message, name, from_email),
                settings.DEFAULT_FROM_EMAIL,
                [from_email],
                fail_silently=False,
            )

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'from_email',
            'subject',
            'message',
            'cc_sender',
            'captcha',
            HTML(render_to_string('account/recaptcha-declaration.html')),
            Submit('submit', 'Send email'),
        )
        self.fields['captcha'].label = False
