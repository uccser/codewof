"""Models for research application."""

from django.db import models
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.urls import reverse
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from codewof.models import Question

User = get_user_model()


class Study(models.Model):
    """A research study."""

    slug = AutoSlugField(populate_from='title', always_update=True, null=True)
    title = models.CharField(max_length=200)
    description = RichTextUploadingField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    visible = models.BooleanField(
        default=False,
        help_text='Set to true when study should be listed to users.',
    )
    consent_form = models.CharField(
        max_length=200,
        help_text='Name of class for consent form.',
        blank=True,
    )

    def get_next_group(self):
        """Get group with lowest user count for next user to join."""
        groups = self.groups.annotate(
            Count('registrations')).order_by('registrations__count')
        return groups[0]

    def get_absolute_url(self):
        """Return URL of study on the website.

        Returns:
            URL as a string.
        """
        return reverse('research:study', kwargs={'pk': self.pk})

    def get_absolute_consent_url(self):
        """Return URL of study on the website.

        Returns:
            URL as a string.
        """
        return reverse('research:study_consent_form', kwargs={'pk': self.pk})

    def __str__(self):
        """Text representation of a study."""
        return self.title

    class Meta:
        """Meta information for class."""

        verbose_name = 'study'
        verbose_name_plural = 'studies'
        ordering = ['start_date', 'end_date']


class StudyGroup(models.Model):
    """A group for a research study."""

    title = models.CharField(
        max_length=200,
        help_text='Name of group, hidden from users and source control.'
    )
    study = models.ForeignKey(
        Study,
        related_name='groups',
        on_delete=models.CASCADE
    )
    questions = models.ManyToManyField(
        Question,
        related_name='groups',
        blank=True,
    )

    def __str__(self):
        """Text representation of a study."""
        return "{} - {}".format(self.study.title, self.title)


class StudyRegistration(models.Model):
    """An registration for an research study."""

    datetime = models.DateTimeField(auto_now_add=True)
    send_study_results = models.BooleanField(default=False)
    study_group = models.ForeignKey(
        StudyGroup,
        related_name='registrations',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='registrations',
        on_delete=models.CASCADE
    )
