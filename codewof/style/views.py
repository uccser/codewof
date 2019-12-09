"""Views for style application."""

from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
)


class HomeView(TemplateView):
    """View for style homepage."""

    template_name = 'style/home.html'
