"""URL routing for codeWOF application."""

from django.urls import path

from . import views

app_name = 'codewof'
urlpatterns = [
    path('', views.IndexView.as_view(), name="home"),
    path('users/profile/', views.ProfileView.as_view(), name="profile"),
    path('questions/', views.QuestionListView.as_view(), name="question_list"),
    path('questions/<int:pk>/', views.QuestionView.as_view(), name="question"),
    path('ajax/save_question_attempt/', views.save_question_attempt, name='save_question_attempt'),
    # path('skills/<int:pk>/', views.SkillView.as_view(), name="skill"),
    # path('random/<int:current_question_id>/', views.get_random_question, name='random'),
    # path('ajax/send_code/', views.send_code, name="send_code"),
    # path('ajax/send_solution/', views.send_solution, name="send_solution"),
    # path('ajax/get_output/', views.get_output, name="get_output"),
    # path('ajax/save_goal_choice/', views.save_goal_choice, name="save_goal_choice"),
]
