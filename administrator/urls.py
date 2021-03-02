from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='adminhome'),
    path('students/', views.students, name='adminstudents'),
    path('instructors/', views.instructors, name='admininstructors'),
    path('courses/', views.courses, name='admincourses'),
    path('create-student/', views.create_student, name='createstudent'),
    path('create-instructor/', views.create_instructor, name='createinstructor'),
    path('create-course/', views.create_course, name='createcourse'),
    path('manage-registration', views.manage_registration, name='manageregistration'),
    path('edit-course/<int:courseid>/', views.edit_course, name='editcourse'),
    path('create-section/<int:courseid>/', views.create_section, name='createsection'),
    path('semester-courses', views.semester_courses, name='semestercourses'),
    path('sections/<int:courseid>/', views.sections, name='sections'),
]