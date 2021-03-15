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
    path('course/<int:course_id>/<int:coursesection_id>/', views.course, name="coursePage"),
    path('schedule',views.schedule, name='schedule'),
    path('adviseeList',views.adviseeList, name='adviseeList'),
    path('advisee/<int:student_id>/',views.advisee),
    path('registration', views.registration, name='registration'),
    path('announcements/<int:coursesection_id>/', views.announcements, name='announcements'),
    path('assignments/<int:coursesection_id>/', views.assignments, name='assignments'),
    path('mysubmissions/', views.mysubmissions, name='mysubmissions'),
    path('assignment/<int:coursesection_id>/<int:assignment_id>/', views.assignment, name='assignment'),
    path('cexam',views.cexam,name='cexam'),
    path('quiz', views.quiz, name='quiz'),
    path('documents', views.documents, name='documents'),
    path('semester-courses/<school>/', views.semester_courses, name='semestercourses'),
    path('requirements-courses/<school>/', views.requirements_courses, name='requirementscourses'),
]
