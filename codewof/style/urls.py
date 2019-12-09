"""URL routing for style application."""

from django.urls import path
from . import views

app_name = 'style'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path('<slug:language>/', views.LanguageView.as_view(), name='language'),
]
