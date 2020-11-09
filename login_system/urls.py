from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login, name='login'),
    path('grade',views.grade, name='grade'),
    path('profile',views.profile, name='profile'),
    path('logout',views.logout, name='logout'),
    path('participants',views.participants, name='participants'),
    path('course/<int:course_id>/<int:coursesection_id>/', views.course),
]
