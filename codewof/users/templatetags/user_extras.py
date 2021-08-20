"""Module for the get_attempt_like_users_for_group tag."""

from django import template

register = template.Library()


@register.simple_tag
def get_attempt_like_users_for_group(attempt, group_pk):
    """
    Call the get_like_users_for_group method for the attempt.

    :param attempt: The attempt to get the like users for.
    :param group_pk: The group pk to pass to the method call.
    :return: The result of get_like_users_for_group (queryset of Users).
    """
    return attempt.get_like_users_for_group(group_pk)
