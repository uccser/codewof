"""URL routing for research application."""

from django.conf.urls import url
from django.urls import path
from research import settings
from research import views


app_name = 'research'
if settings.RESEARCH_ACTIVE:
    urlpatterns = [
        # User views
        path('', views.StudyDetailView.as_view(), name='home'),
        path('consent-form/', views.StudyConsentFormView.as_view(), name='consent_form'),
        # # Admin views
        # path('study/admin/', views.StudyAdminView.as_view(), name='study_admin'),
    ]
else:
    urlpatterns = []
