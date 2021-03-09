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

    if request.method == 'POST':
        post_id = request.POST.get('post_id', None)
        if post_id == 'Edit':
            student = request.POST.get('student', None)
            return redirect('editstudent', studentid=student)
        elif post_id == 'Assign':
            student = request.POST.get('student', None)
            return redirect('assignadvisor', studentid=student)
        elif post_id == 'Delete':
            student = request.POST.get('student', None)
            student = Student.objects.filter(studentid=student).first()
            student.delete()
    return render(request,'adminstudents.html', {"students":students})

def assign_advisor(request, studentid):
    student = Student.objects.filter(studentid=studentid).first()
    instructors = Instructor.objects.all()
    advisors = Advice.objects.filter(student_studentid=student.studentid).all()

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if post_id == 'Save':
            instructor = request.POST.get('instructor', None)
            instructor = Instructor.objects.filter(instructorid=instructor).first()
            try:
                new_advice = Advice(instructor_instructorid=instructor, student_studentid=student)
                new_advice.save()
            except:
                render(request, 'assignadvisor.html', {'student':student, 'instructors':instructors, 'advisors':advisors})
        elif post_id == 'Delete':
            instructor = request.POST.get('instructor', None)
            instructor = Instructor.objects.filter(instructorid=instructor).first()
            advice = Advice.objects.filter(instructor_instructorid=instructor, student_studentid=student)  
            advice.delete()          

    return render(request, 'assignadvisor.html', {'student':student, 'instructors':instructors, 'advisors':advisors})

def edit_student(request, studentid):
    student = Student.objects.filter(studentid=studentid).first()
    user = student.user_userid
    departments = Department.objects.all()

    if request.method == 'POST':
        user.role = request.POST.get('new-content', None)
        user.first_name = request.POST.get('first_name', None)
        user.last_name = request.POST.get('last_name', None)
        user.email = request.POST.get('email', None)
        user.password = request.POST.get('password', None)
        user.gender = request.POST.get('gender', None)
        department_name = request.POST.get('department', None)
        user.school_name = Department.objects.filter(name=department_name).first().school_name
        user.department_name = Department.objects.filter(name=department_name).first()
        user.save()

        student.level = request.POST.get('level', None)
        student.year_of_study = request.POST.get('year_of_study', None)
        student.academic_status = request.POST.get('academic_status', None)
        student.save()
    return render(request, 'editstudent.html', {'student':student, 'user':user, 'departments':departments})

def instructors(request):
    instructors = Instructor.objects.all()

    if request.method == 'POST':
        post_id = request.POST.get('post_id', None)
        if post_id == 'Edit':
            instructor = request.POST.get('instructor', None)
            return redirect('editinstructor', instructorid=instructor)
        elif post_id == 'Assign':
            instructor = request.POST.get('instructor', None)
            return redirect('assignadvisee', instructorid=instructor)
        elif post_id == 'Delete':
            instructor = request.POST.get('instructor', None)
            instructor = Instructor.objects.filter(instructorid=instructor).first()
            instructor.delete()
    return render(request,'admininstructors.html', {"instructors":instructors})

def assign_advisee(request, instructorid):
    instructor = Instructor.objects.filter(instructorid=instructorid).first()
    students = Student.objects.all()
    advisees = Advice.objects.filter(instructor_instructorid=instructor.instructorid).all()

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if post_id == 'Save':
            student = request.POST.get('student', None)
            student = Student.objects.filter(studentid=student).first()
            try:
                new_advice = Advice(instructor_instructorid=instructor, student_studentid=student)
                new_advice.save()
            except:
                render(request, 'assignadvisee.html', {'instructor':instructor, 'students':students, 'advisees':advisees})
        elif post_id == 'Delete':
            student = request.POST.get('student', None)
            student = Student.objects.filter(studentid=student).first()
            advice = Advice.objects.filter(instructor_instructorid=instructor, student_studentid=student)  
            advice.delete() 
    return render(request, 'assignadvisee.html', {'instructor':instructor, 'students':students, 'advisees':advisees})

def edit_instructor(request, instructorid):
    instructor = Instructor.objects.filter(instructorid=instructorid).first()
    user = instructor.user_userid
    departments = Department.objects.all()

    if request.method == 'POST':
        user.role = request.POST.get('new-content', None)
        user.first_name = request.POST.get('first_name', None)
        user.last_name = request.POST.get('last_name', None)
        user.email = request.POST.get('email', None)
        user.password = request.POST.get('password', None)
        user.gender = request.POST.get('gender', None)
        department_name = request.POST.get('department', None)
        user.school_name = Department.objects.filter(name=department_name).first().school_name
        user.department_name = Department.objects.filter(name=department_name).first()
        user.save()

        instructor.position = request.POST.get('position', None)
        instructor.save()
    return render(request, 'editinstructor.html', {'instructor':instructor, 'user':user, 'departments':departments})

def courses(request):
    courses = Course.objects.all()

    if request.method == 'POST':
        post_id = request.POST.get('post_id', None)
        if post_id == 'Edit':
            course = request.POST.get('course', None)
            return redirect('editcourse', courseid=course)
        elif post_id == 'Sections':
            course = request.POST.get('course', None)
            return redirect('sections', courseid=course)
        elif post_id == 'Add':
            course = request.POST.get('course', None)
            return redirect('createsection', courseid=course)
        elif post_id == 'Priority':
            course = request.POST.get('course', None)
            return redirect('addpriority', courseid=course)
        elif post_id == 'Delete':
            course = request.POST.get('course', None)
            course = Course.objects.filter(courseid=course).first()
            course.delete()
    return render(request,'admincourses.html', {"courses":courses})

def add_priority(request, courseid):
    course = Course.objects.filter(courseid=courseid).first()
    departments = Department.objects.all()
    priorities = Priority.objects.filter(course_courseid=course).order_by('type').all()
    if request.method == 'POST':
        post_id = request.POST.get('post_id', None)
        if  post_id == 'Save':
            department = request.POST.get('department', None)
            department = Department.objects.filter(name=department).first()
            year = request.POST.get('year', None)
            type = request.POST.get('type', None)
            try:
                new_priority = Priority(course_courseid=course, department_name=department, year=year, type=type)
                new_priority.save()
            except:
                priority = Priority.objects.filter(course_courseid=course, department_name=department, year=year).first()
                priority.type = type
                priority.save()
        elif post_id == 'Delete':
            priority = request.POST.get('priority', None)
            priority = Priority.objects.filter(id=priority).first()
            priority.delete()

    return render(request, 'addpriority.html', {'course':course, 'departments':departments, 'priorities':priorities})

def sections(request, courseid):
    course = Course.objects.filter(courseid=courseid).first()
    if request.method == 'POST':
        post_id = request.POST.get('post_id', None)
        if post_id == 'Edit':
            section = request.POST.get('section', None)
            return redirect('editsection', sectionid=section)
        elif post_id == 'Delete':
            section = request.POST.get('section', None)
            section = Coursesection.objects.filter(sectionid=section).first()
            section.delete()

    sections_days = []
    days_dic = {'1':'Monday', '2':'Tuesday', '3':'Wednesday', '4':'Thursday', '5':'Friday', '6':'Saturday'}
    sections = Coursesection.objects.filter(course_courseid=courseid).all()
    for sec in sections:
        days = list(Sectionday.objects.filter(coursesection_sectionid=sec.sectionid).all())
        for i, day in enumerate(days):
            days[i] = days_dic[day.day]
        days = ' '.join(days)
        sections_days.append([sec, days])
    return render(request, 'sections.html', {'course':course, 'sections':sections_days})

def edit_section(request, sectionid):
    section = Coursesection.objects.filter(sectionid=sectionid).first()
    days = list(Sectionday.objects.filter(coursesection_sectionid=section.sectionid).all())
    start = str(section.start_time)
    end = str(section.end_time)
    for i, day in enumerate(days):
        days[i] = day.day

    if request.method == 'POST':
        section.num_type = request.POST.get('num_type', None)
        section.start_time = request.POST.get('start_time', None)
        section.end_time = request.POST.get('end_time', None)
        section.semester = request.POST.get('semester', None)
        section.year = request.POST.get('year', None)
        section.capacity = request.POST.get('capacity', None)
        section.room = request.POST.get('room', None)
        section.total_points = request.POST.get('total_points', None)
        section.save()
        days = list(Sectionday.objects.filter(coursesection_sectionid=section.sectionid).all())
        for day in days:
            day.delete()
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
        days = list(Sectionday.objects.filter(coursesection_sectionid=section.sectionid).all())
        for i, day in enumerate(days):
                days[i] = day.day
        return redirect('sections', courseid=section.course_courseid.courseid)

    return render(request, 'editsection.html', {'section':section, 'days':days, 'start':start, 'end':end})

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
        return redirect('sections', courseid=course.courseid)

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
    departments = Department.objects.all()

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
    return render(request,'createstudent.html', {"departments":departments})

def create_instructor(request):
    departments = Department.objects.all()

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
    return render(request,'createinstructor.html', {"departments":departments})

def create_course(request):
    departments = Department.objects.all()

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
    return render(request,'createcourse.html', {"departments":departments})

def manage_registration(request):
    registrations = Registrationdate.objects.all()

    if request.method == 'POST':
        registrationid = request.POST.get('regId', None)
        open_time = request.POST.get('openAt', None)
        close_time = request.POST.get('closeAt', None)

        registration = Registrationdate.objects.get(registrationid=registrationid)
        registration.open_time = open_time
        registration.close_time = close_time
        registration.save()
    return render(request, 'adminregistration.html', {"registrations":registrations})

