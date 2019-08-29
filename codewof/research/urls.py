"""URL routing for research application."""

from django.urls import path
from research import views


app_name = 'research'
urlpatterns = [
    path('', views.StudyListView.as_view(), name='home'),
    path('study/<int:pk>/', views.StudyDetailView.as_view(), name='study'),
    path('study/<int:pk>/admin/', views.StudyAdminView.as_view(), name='study_admin'),
    path('study/<int:pk>/admin/csv/', views.study_admin_csv_download_view, name='study_admin_csv'),
    path('study/<int:pk>/consent-form/', views.StudyConsentFormView.as_view(), name='study_consent_form'),
]
