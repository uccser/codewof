"""URL routing for users application."""

from django.urls import path
from . import views


app_name = "users"
urlpatterns = [
    path("dashboard/", view=views.UserDetailView.as_view(), name="dashboard"),
    path("redirect/", view=views.UserRedirectView.as_view(), name="redirect"),
    path("update/", view=views.UserUpdateView.as_view(), name="update"),
    path("achievements/", view=views.UserAchievementsView.as_view(), name="achievements"),
    path("groups/add/", view=views.GroupCreateView.as_view(), name="groups-add"),
    path("groups/<int:pk>/edit/", view=views.GroupUpdateView.as_view(), name="groups-edit"),
    path("groups/<int:pk>/", view=views.GroupDetailView.as_view(), name="groups-detail"),
    path("groups/<int:pk>/delete/", view=views.GroupDeleteView.as_view(), name="groups-delete"),
]
