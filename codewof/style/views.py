"""Views for style application."""

import json
from django.conf import settings
from django.http import JsonResponse, Http404
from django.views.generic import (
    TemplateView,
    ListView,
)
from style.style_checkers.python3 import python3_style_check
from style.models import Error
from style.utils import (
    render_results_as_html,
    render_results_as_text,
    get_language_info,
    CHARACTER_DESCRIPTIONS,
)

LANGUAGE_PATH_TEMPLATE = 'style/{}.html'


class HomeView(ListView):
    """View for style homepage."""

    template_name = 'style/home.html'
    context_object_name = 'languages'

    def get_queryset(self):
        """Get iterate of languages for page."""
        return settings.STYLE_CHECKER_LANGUAGES


class LanguageStyleCheckerView(TemplateView):
    """View for a language style checker."""

    template_name = 'style/language.html'

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        language_slug = self.kwargs.get('language', '')
        language_info = get_language_info(language_slug)
        # If language not found
        if not language_info:
            raise Http404
        context['language'] = language_info
        context['language_header'] = 'style/language-components/{}-header.html'.format(language_slug)
        context['language_subheader'] = 'style/language-components/{}-subheader.html'.format(language_slug)
        context['language_js'] = 'js/style_checkers/{}.js'.format(language_slug)
        context['MAX_CHARACTER_COUNT'] = settings.STYLE_CHECKER_MAX_CHARACTER_COUNT
        return context


class LanguageStatisticsView(TemplateView):
    """View for a language statistics."""

    template_name = 'style/language-statistics.html'

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        language_slug = self.kwargs.get('language', '')
        language_info = get_language_info(language_slug)
        # If language not found
        if not language_info:
            raise Http404
        context['language'] = language_info
        context['language_header'] = 'style/language-components/{}-header.html'.format(language_slug)
        context['issues'] = Error.objects.filter(language=language_slug).order_by('-count', 'code')
        if context['issues']:
            context['max_count'] = context['issues'][0].count
        context['characters'] = list(CHARACTER_DESCRIPTIONS.keys())
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
                result_data = python3_style_check(user_code)
                result['success'] = True
            else:
                # TODO: else raise error language isn't supported
                pass
            result['result_html'] = render_results_as_html(result_data)
            result['result_text'] = render_results_as_text(user_code, result_data)
    return JsonResponse(result)
