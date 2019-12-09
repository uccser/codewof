"""Views for style application."""

from django.urls import reverse_lazy
from django.http import Http404
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.views.generic import (
    TemplateView,
)

LANGUAGE_PATH_TEMPLATE = 'style/{}.html'


class HomeView(TemplateView):
    """View for style homepage."""

    template_name = 'style/home.html'


class LanguageStyleCheckerView(TemplateView):
    """View for a language style checker."""

    def get_template_names(self):
        language_slug = self.kwargs.get('language', '')
        template_path = LANGUAGE_PATH_TEMPLATE.format(language_slug)
        try:
            get_template(template_path)
        except TemplateDoesNotExist:
            raise Http404
        else:
            return [template_path]
