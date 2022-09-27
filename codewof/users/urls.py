"""URL routing for users application."""

from django.urls import path
from django.conf import settings
from rest_framework import routers
from . import views

app_name = "users"

router = routers.SimpleRouter()
if not settings.PRODUCTION_ENVIRONMENT:
    router.register(r'users/users', views.UserAPIViewSet)
    router.register(r'users/user-types', views.UserTypeAPIViewSet)
    router.register(r'users/groups', views.GroupAPIViewSet)
    router.register(r'users/memberships', views.MembershipAPIViewSet)
    router.register(r'users/group-roles', views.GroupRoleAPIViewSet)
    router.register(r'users/invitations', views.InvitationAPIViewSet)


urlpatterns = [
    path("dashboard/", view=views.UserDetailView.as_view(), name="dashboard"),
    path("redirect/", view=views.UserRedirectView.as_view(), name="redirect"),
    path("update/", view=views.UserUpdateView.as_view(), name="update"),
    path("achievements/", view=views.UserAchievementsView.as_view(), name="achievements"),
    path("groups/add/", view=views.GroupCreateView.as_view(), name="groups-add"),
    path("groups/<int:pk>/edit/", view=views.GroupUpdateView.as_view(), name="groups-edit"),
    path("groups/<int:pk>/", view=views.GroupDetailView.as_view(), name="groups-detail"),
    path("groups/<int:pk>/delete/", view=views.GroupDeleteView.as_view(), name="groups-delete"),
    path("groups/<int:pk>/memberships/", view=views.update_memberships, name="groups-memberships-update"),
    path("memberships/<int:pk>/delete/", view=views.MembershipDeleteView.as_view(), name="groups-memberships-delete"),
    path("groups/<int:pk>/memberships/invite/", view=views.create_invitations, name="groups-memberships-invite"),
    path("invitations/<int:pk>/accept/", view=views.accept_invitation, name="groups-invitations-accept"),
    path("invitations/<int:pk>/reject/", view=views.reject_invitation, name="groups-invitations-reject"),
    path("groups/<int:pk>/emails/", view=views.get_group_emails, name="groups-emails")
]
