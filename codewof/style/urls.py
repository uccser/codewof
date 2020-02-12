"""URL routing for style application."""

from django.urls import path
from . import views

app_name = 'style'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<slug:language>/', views.LanguageStyleCheckerView.as_view(), name='language'),
    path('ajax/check/', views.check_code, name='check_code'),
]
