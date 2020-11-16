from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('course/', views.course, name='course'),
    path('', views.login, name='login'),
    path('grades',views.grades, name='grades'),
    path('profile',views.profile, name='profile'),
    path('logout',views.logout, name='logout'),
    path('participants/<int:coursesection_id>/',views.participants),
    path('course/<int:course_id>/<int:coursesection_id>/', views.course),
    path('schedule',views.schedule, name='schedule'),
    path('adviseeList',views.adviseeList, name='adviseeList'),
    path('download/<int:file_id>/', views.download, name='download'),
]
