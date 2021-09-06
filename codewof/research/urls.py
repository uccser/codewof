"""URL routing for research application."""

from django.urls import path
from research import settings
from research import views
from rest_framework import routers

app_name = 'research'
router = routers.SimpleRouter()

if settings.RESEARCH_ACTIVE:
    router.register(r'research/study-registrations', views.StudyRegistrationAPIViewSet)

    urlpatterns = [
        # User views
        path('', views.StudyDetailView.as_view(), name='home'),
        path('consent-form/', views.StudyConsentFormView.as_view(), name='consent_form'),
    ]
else:
    urlpatterns = []
