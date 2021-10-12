"""Utilities for the User app, primarily for views."""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from django.urls import reverse


def send_invitation_email(invitee, inviter, group_name, email):
    """
    Create and send an invitation email.

    :param invitee: The User receiving the invite, which is null if the User does not exist yet.
    :param inviter: The User creating the invite.
    :param group_name: The name of the Group to be joined.
    :param email: The invitee's email address.
    :return:
    """
    if invitee is None:
        html = create_invitation_html(False, None, inviter.first_name + " " + inviter.last_name, group_name, email)
        plain = create_invitation_plaintext(False, None, inviter.first_name + " " + inviter.last_name, group_name,
                                            email)
    else:
        html = create_invitation_html(True, invitee.first_name, inviter.first_name + " " + inviter.last_name,
                                      group_name, email)
        plain = create_invitation_plaintext(True, invitee.first_name, inviter.first_name + " " + inviter.last_name,
                                            group_name, email)

    send_mail(
        'CodeWOF Invitation',
        plain,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
        html_message=html
    )


def create_invitation_plaintext(user_exists, invitee_name, inviter_name, group_name, email):
    """
    Build the plaintext for the invitation email, which is different depending if an account with the email exists.

    :param user_exists: Whether a User object with this email exists.
    :param invitee_name: The name of the invitee.
    :param inviter_name: The name of the inviter.
    :param group_name: The name of the group.
    :param email: The email address.
    :return:
    """
    if user_exists:
        url = settings.CODEWOF_DOMAIN + reverse('users:dashboard')
        plaintext = "Hi {},\n\n{} has invited you to join the Group '{}'. Click the link below to sign in. You will "\
                    "see your invitation in the dashboard, where you can join the group.\n\n{}\n\nThanks,\nThe "\
                    "Computer Science Education Research Group".format(invitee_name, inviter_name, group_name, url)
    else:
        url = settings.CODEWOF_DOMAIN + reverse('account_signup')
        plaintext = "Hi,\n\n{} has invited you to join the Group '{}'. CodeWOF helps you maintain your programming "\
                    "fitness with short daily programming exercises. With a free account you can save your progress "\
                    "and track your programming fitness over time. Click the link below to make an account, using "\
                    "the email {}. You will see your invitation in the dashboard, where you can join the group. "\
                    "If you already have a CodeWOF account, then add {} to your profile to make the invitation "\
                    "appear.\n\n{}\n\nThanks,\nThe Computer Science Education Research Group"\
            .format(inviter_name, group_name, email, email, url)
    return plaintext


def create_invitation_html(user_exists, invitee_name, inviter_name, group_name, email):
    """
    Build the html for the invitation email, which is different depending if an account with the email exists or not.

    :param user_exists: Whether a User object with this email exists.
    :param invitee_name: The name of the invitee.
    :param inviter_name: The name of the inviter.
    :param group_name: The name of the group.
    :param email: The email address.
    :return:
    """
    email_template = get_template("users/group_invitation.html")
    if user_exists:
        message = "{} has invited you to join the Group '{}'. Click the link below to sign in. You will "\
                  "see your invitation in the dashboard, where you can join the group."\
            .format(inviter_name, group_name)
        url = settings.CODEWOF_DOMAIN + reverse('users:dashboard')
        html = email_template.render({"user_exists": user_exists, "invitee_name": invitee_name, "message": message,
                                      "url": url, "button_text": "Sign In"})
    else:
        message = "{} has invited you to join the Group '{}'. CodeWOF helps you maintain your "\
                  "programming fitness with short daily programming exercises. With a free account you can save your "\
                  "progress and track your programming fitness over time. Click the link below to make an account,"\
                  " using the email {}. You will see your invitation in the dashboard, where you can join the group. "\
                  "If you already have a CodeWOF account, then add {} to your profile to make the invitation appear."\
            .format(inviter_name, group_name, email, email)
        url = settings.CODEWOF_DOMAIN + reverse('account_signup')
        html = email_template.render({"user_exists": user_exists, "invitee_name": invitee_name, "message": message,
                                      "url": url, "button_text": "Sign Up"})
    return html
