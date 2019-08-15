"""Views for users application."""

from random import Random
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, RedirectView, UpdateView
from users.forms import UserChangeForm
from programming.models import Question, Attempt
from programming import settings
from research.models import StudyRegistration

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    """View for a user's dashboard."""

    model = User
    context_object_name = 'user'
    template_name = 'users/dashboard.html'

    def get_object(self):
        """Get object for template."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        today = now.date()

        if self.request.user.is_authenticated:
            # Look for active study registration
            try:
                study_registration = StudyRegistration.objects.get(
                    user=self.request.user,
                    study_group__study__start_date__lte=now,
                    study_group__study__end_date__gte=now,
                )
            except ObjectDoesNotExist:
                study_registration = None

        # Get questions not attempted before today
        if study_registration:
            questions = study_registration.study_group.questions()
        else:
            questions = Question.objects.all()
        # TODO: Also filter by questions added before today
        questions = questions.filter(
            Q(attempt__isnull=True) |
            (Q(attempt__passed_tests=False) & Q(attempt__datetime__date__lte=today)) |
            (Q(attempt__passed_tests=True) & Q(attempt__datetime__date=today))
        ).order_by('pk').distinct('pk').select_subclasses()
        questions = list(questions)

        # Randomly pick 3 based off seed of todays date
        if len(questions) > 0:
            random_seeded = Random(today)
            number_to_do = min(len(questions), settings.QUESTIONS_PER_DAY)
            todays_questions = random_seeded.sample(questions, number_to_do)
            all_complete = True
            for question in todays_questions:
                question.completed = Attempt.objects.filter(
                    profile=self.request.user.profile,
                    question=question,
                    passed_tests=True,
                ).exists()
                if all_complete and not question.completed:
                    all_complete = False
        else:
            todays_questions = list()
            all_complete = False
        context['questions_to_do'] = todays_questions
        context['all_complete'] = all_complete

        # Show studies
        studies = self.request.user.user_type.studies.filter(
            visible=True,
            groups__isnull=False,
        ).distinct()
        # TODO: Simplify to one database query
        for study in studies:
            study.registered = StudyRegistration.objects.filter(
                user=self.request.user,
                study_group__in=study.groups.all(),
            ).exists()
        context['studies'] = studies
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating user data."""

    model = User
    fields = ['first_name', 'last_name', 'user_type']

    def get_success_url(self):
        """URL to route to on successful update."""
        return reverse('users:profile')

    def get_object(self):
        """Object to perform update with."""
        return User.objects.get(pk=self.request.user.pk)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """View for redirecting to a user's webpage."""

    permanent = False

    def get_redirect_url(self):
        """URL to redirect to."""
        return reverse("users:profile")
