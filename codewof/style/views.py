"""Views for style application."""

import json
from django.conf import settings
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse, HttpResponse
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.views.generic import (
    TemplateView,
)
from style.style_checkers.python import python_style_check
from style.utils import (
    render_results_as_html,
    render_results_as_text,
    update_error_counts,
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

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        context['MAX_CHARACTER_COUNT'] = settings.STYLE_CHECKER_MAX_CHARACTER_COUNT
        return context


def check_code(request):
    """Check the user's code for style issues.

    Args:
        request (Request): AJAX request from user.

    Returns:
        JSON response with result.
    """
    result = {
        'success': False,
    }
    if request.is_ajax():
        request_json = json.loads(request.body.decode('utf-8'))
        user_code = request_json['user_code']
        if 0 < len(user_code) <= settings.STYLE_CHECKER_MAX_CHARACTER_COUNT:
            language = request_json['language']
            if language == 'python3':
                result_data = python_style_check(user_code)
                result['success'] = True
            else:
                # TODO: else raise error language isn't supported
                pass
            update_error_counts(language, result_data)
            result['result_html'] = render_results_as_html(result_data)
            result['result_text'] = render_results_as_text(user_code, result_data)
    return JsonResponse(result)
