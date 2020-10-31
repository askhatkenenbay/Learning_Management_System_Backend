from django.urls import path
from . import views

urlpatterns = [
    path('', views.quizzes, name='quizzes'),
    path('depression-quiz', views.depression, name='depression'),
    path('anxiety-quiz', views.anxiety, name='anxiety'),
   
]