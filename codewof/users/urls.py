"""URL routing for users application."""

from django.urls import path
from . import views


app_name = "users"
urlpatterns = [
    path("profile/", view=views.UserDetailView.as_view(), name="profile"),
    path("redirect/", view=views.UserRedirectView.as_view(), name="redirect"),
    path("update/", view=views.UserUpdateView.as_view(), name="update"),
]
