"""Signals for the user application."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

user_model = get_user_model()


@receiver(post_save, sender=user_model)
def create_user_profile(sender, instance, created, **kwargs):
    """Add automated value for username."""
    if created:
        instance.username = 'user{}'.format(instance.id)
        instance.save()
