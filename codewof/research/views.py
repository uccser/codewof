"""Views for research application."""

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from research.models import (
    Study,
)


class StudyListView(generic.ListView):
    """Homepage for research studies."""

    model = Study
    context_object_name = 'studies'
    template_name = 'research/home.html'

    def get_queryset(self):
        """Return studies objects for page.

        Returns:
            Study queryset.
        """
        studies = Study.objects.filter(visible=True).order_by('start_date')
        return studies


class StudyDetailView(generic.DetailView):
    """Homepage for research studies."""

    model = Study
    context_object_name = 'study'

    def get_queryset(self):
        """Return studies objects for page.

        Returns:
            Study queryset.
        """
        studies = Study.objects.filter(visible=True).order_by('start_date')
        return studies
