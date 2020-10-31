from django.urls import path
from . import views

urlpatterns = [
    path('', views.chal_list, name='chal_list'),
    path('breathing-exercise/', views.breath, name='breath'),
    path('30-minutes-of-yoga/', views.yoga, name='yoga'),
    path('night-with-friends/', views.friends, name='friends'),
    path('call-parents/', views.parents, name='parents'),
    path('meet-your-floormate/', views.floormate, name='floormate'),
    path('write-good-thing/', views.good, name='good'),    
]