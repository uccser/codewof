"""Views for style application."""

import json
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.views.generic import (
    TemplateView,
)
from style.style_checkers.python import python_style_check

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
        # TODO: Check submission length
        request_json = json.loads(request.body.decode('utf-8'))
        user_code = request_json['user_code']
        language = request_json['language']
        if language == 'python3':
            result_html = python_style_check(user_code)
            result['success'] = True
            result['feedback_html'] = result_html
        # else raise error language isn't supported
    return JsonResponse(result)
