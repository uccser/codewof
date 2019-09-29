"""URL routing for programming application."""

from django.urls import include, path
from rest_framework import routers

from . import views
from research import views as research_views
from users import views as user_views

router = routers.DefaultRouter()
router.register(r'api-questions', views.QuestionAPIViewSet)
router.register(r'api-studies', research_views.StudyAPIViewSet)
router.register(r'api-attempts', views.AttemptAPIViewSet)
router.register(r'api-users', user_views.UserAPIViewSet)

app_name = 'programming'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('', include(router.urls)),
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/create/', views.CreateView.as_view(), name='create'),
    path('questions/<int:pk>/', views.QuestionView.as_view(), name='question'),
    path('ajax/save_question_attempt/', views.save_question_attempt, name='save_question_attempt'),
    # path('skills/<int:pk>/', views.SkillView.as_view(), name="skill"),
    # path('random/<int:current_question_id>/', views.get_random_question, name='random'),
    # path('ajax/send_code/', views.send_code, name="send_code"),
    # path('ajax/send_solution/', views.send_solution, name="send_solution"),
    # path('ajax/get_output/', views.get_output, name="get_output"),
    # path('ajax/save_goal_choice/', views.save_goal_choice, name="save_goal_choice"),
]
