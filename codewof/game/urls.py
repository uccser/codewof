"""URL routing for game application."""

from django.urls import path
from django.conf import settings
from rest_framework import routers
from game import views

app_name = 'game'

router = routers.SimpleRouter()

urlpatterns = [

]
