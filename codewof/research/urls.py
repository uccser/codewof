"""URL routing for research application."""

from django.urls import path

from . import views

app_name = 'research'
urlpatterns = [
    path('', views.StudyListView.as_view(), name='home'),
    path('study/<int:pk>', views.StudyDetailView.as_view(), name='study'),
]
