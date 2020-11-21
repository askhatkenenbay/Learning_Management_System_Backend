from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from alldata.models import *


def home(request):
    return render(request,'adminhome.html')

def students(request):
    students = Student.objects.all()
    return render(request,'adminstudents.html', {"students":students})

def instructors(request):
    instructors = Instructor.objects.all()
    return render(request,'admininstructors.html', {"instructors":instructors})

def courses(request):
    courses = Course.objects.all()
    return render(request,'admincourses.html', {"courses":courses})

def create_student(request):
    if request.method == 'POST':
        role = request.POST.get('new-content', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        gender = request.POST.get('gender', None)
        department_name = request.POST.get('department', None)
        school_name = Department.objects.filter(name=department_name).first().school_name
        department_name = Department.objects.filter(name=department_name).first()

        new_user = User(role=role, first_name=first_name, last_name=last_name, email=email, password=password, gender=gender, department_name=department_name, school_name=school_name)
        new_user.save()

        level = request.POST.get('level', None)
        year_of_study = request.POST.get('year_of_study', None)
        academic_status = request.POST.get('academic_status', None)

        new_student = Student(user_userid=new_user, level=level, year_of_study=year_of_study, academic_status=academic_status)
        new_student.save()

    departments = Department.objects.all()
    return render(request,'createstudent.html', {"departments":departments})

def create_instructor(request):
    if request.method == 'POST':
        role = request.POST.get('new-content', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        gender = request.POST.get('gender', None)
        department_name = request.POST.get('department', None)
        school_name = Department.objects.filter(name=department_name).first().school_name
        department_name = Department.objects.filter(name=department_name).first()

        new_user = User(role=role, first_name=first_name, last_name=last_name, email=email, password=password, gender=gender, department_name=department_name, school_name=school_name)
        new_user.save()

        position = request.POST.get('position', None)

        new_instructor = Instructor(user_userid=new_user, position=position)
        new_instructor.save()

    departments = Department.objects.all()
    return render(request,'createinstructor.html', {"departments":departments})

def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title', None)
        course_code = request.POST.get('course_code', None)
        credits = request.POST.get('credits', None)
        description = request.POST.get('description', None)
        department_name = request.POST.get('department', None)
        department_name = Department.objects.filter(name=department_name).first()
        level = request.POST.get('level', None)

        new_course = Course(title=title, course_code=course_code, credits=credits, description=description, department_name=department_name, level=level)
        new_course.save()

    departments = Department.objects.all()
    return render(request,'createcourse.html', {"departments":departments})

