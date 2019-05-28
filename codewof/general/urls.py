"""URL routing for general application."""

from django.urls import path
from . import views

app_name = 'general'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact-us/', views.ContactView.as_view(), name='contact'),
    path('contact-us/success/', views.ContactSuccessView.as_view(), name='contact-success'),
    path('faq/', views.FAQView.as_view(), name='faq'),
]
