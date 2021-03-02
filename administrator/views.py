from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from alldata.models import *

year = 2020
semester = "Fall"

def home(request):
    return render(request,'adminhome.html')

def students(request):
    students = Student.objects.all()
    return render(request,'adminstudents.html', {"students":students})

def instructors(request):
    instructors = Instructor.objects.all()
    return render(request,'admininstructors.html', {"instructors":instructors})

def courses(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id', None)
        if post_id == 'Edit':
            course = request.POST.get('course', None)
            return redirect('editcourse', courseid=course)
        elif post_id == 'Add':
            course = request.POST.get('course', None)
            return redirect('createsection', courseid=course)
        elif post_id == 'Delete':
            course = request.POST.get('course', None)
            course = Course.objects.filter(courseid=course).first()
            course.delete()

    courses = Course.objects.all()
    return render(request,'admincourses.html', {"courses":courses})

def create_section(request, courseid):
    course = Course.objects.filter(courseid=courseid).first()
    if request.method == 'POST':
        courseid = course
        num_type = request.POST.get('num_type', None)
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)
        semester = request.POST.get('semester', None)
        year = request.POST.get('year', None)
        capacity = request.POST.get('capacity', None)
        room = request.POST.get('room', None)
        total_points = request.POST.get('total_points', None)

        section = Coursesection(course_courseid=course, num_type=num_type, start_time=start_time, end_time=end_time, semester=semester, year=year, capacity=capacity, room=room, total_points=total_points
            )
        section.save()

        days = []
        days.append(request.POST.get('mn', None) == 'on')
        days.append(request.POST.get('tu', None) == 'on')
        days.append(request.POST.get('wd', None) == 'on')
        days.append(request.POST.get('th', None) == 'on')
        days.append(request.POST.get('fr', None) == 'on')
        days.append(request.POST.get('st', None) == 'on')
        for i, day in enumerate(days):
            if day:
                sectionday = Sectionday(coursesection_sectionid=section, day=str(i+1))
                sectionday.save()

    return render(request, 'createsection.html', {'course':course})

def edit_course(request, courseid):
    course = Course.objects.filter(courseid=courseid).first()
    department = Department.objects.filter(name=course.department_name.name).first()
    departments = Department.objects.all()

    if request.method == 'POST':
        course.title = request.POST.get('title', None)
        course.course_code = request.POST.get('course_code', None)
        course.credits = request.POST.get('credits', None)
        course.description = request.POST.get('description', None)
        department_name = request.POST.get('department', None)
        course.department_name = Department.objects.filter(name=department_name).first()
        course.level = request.POST.get('level', None)
        course.save()

    return render(request, 'editcourse.html', {'course':course, 'department':department, 'departments':departments})

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

def manage_registration(request):
    if request.method == 'POST':
        registrationid = request.POST.get('regId', None)
        open_time = request.POST.get('openAt', None)
        close_time = request.POST.get('closeAt', None)

        registration = Registrationdate.objects.get(registrationid=registrationid)
        registration.open_time = open_time
        registration.close_time = close_time
        registration.save()

    registrations = Registrationdate.objects.all()
    return render(request, 'adminregistration.html', {"registrations":registrations})

def semester_courses(request):
    courses = list(Course.objects.all())
    res_courses = []
    for course in courses:
        sections = list(Coursesection.objects.filter(course_courseid = course.courseid,
                                                     semester = semester,
                                                     year = year))
        if len(sections) != 0:
            res_courses.append(course)
    return render(request, 'semestercourses.html', {"courses":res_courses})

