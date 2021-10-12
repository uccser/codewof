"""Views for general application."""

from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import (
    TemplateView,
    FormView,
)
from general.forms import ContactForm


class HomeView(TemplateView):
    """View for website homepage."""

    template_name = 'general/home.html'


class AboutView(TemplateView):
    """View for website about page."""

    template_name = 'general/about.html'


class PolicyView(TemplateView):
    """View for website policies page."""

    template_name = 'general/policies.html'

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        context['domain'] = settings.CODEWOF_DOMAIN
        return context


class ContactView(FormView):
    """View for website contact page."""

    template_name = 'general/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('general:contact-success')

    def form_valid(self, form):
        """Send email if form is valid."""
        form.send_email()
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    """View for website for contact success page."""

    template_name = 'general/contact-success.html'


class FAQView(TemplateView):
    """View for website FAQ page."""

    template_name = 'general/faq.html'
