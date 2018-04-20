from django.urls import path

from . import views

app_name = 'questions'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('skills/<int:pk>/', views.SkillView.as_view(), name="skill"),
    path('questions/<int:pk>/', views.QuestionView.as_view(), name="question")
]