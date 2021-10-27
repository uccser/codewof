"""URL routing for programming application."""

from django.urls import path
from rest_framework import routers
from programming import views

app_name = 'programming'

router = routers.SimpleRouter()
router.register(r'programming/questions', views.QuestionAPIViewSet)
router.register(r'programming/attempts', views.AttemptAPIViewSet)
router.register(r'programming/profiles', views.ProfileAPIViewSet)

urlpatterns = [
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/create/', views.CreateView.as_view(), name='create'),
    path('questions/<int:pk>/', views.QuestionView.as_view(), name='question'),
    path('ajax/save_question_attempt/', views.save_question_attempt, name='save_question_attempt'),
    path('attempts/<int:pk>/like', views.like_attempt, name='like_attempt'),
    path('attempts/<int:pk>/unlike', views.unlike_attempt, name='unlike_attempt'),
    # path('ajax/save_goal_choice/', views.save_goal_choice, name="save_goal_choice"),
]
