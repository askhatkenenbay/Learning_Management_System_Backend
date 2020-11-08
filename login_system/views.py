from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from .forms import MyUserCreateForm
from alldata.models import User, School, Department, Student,StudentEnrollment,Coursesection,Course, Instructor, CourseInstructor
from django.contrib.auth.decorators import login_required, user_passes_test

noadmin_required = user_passes_test(lambda user: user.role == 'student' or user.role == 'instructor', login_url='/')
def noadmin_required(view_func):
    decorated_view_func = login_required(noadmin_required(view_func))
    return decorated_view_func


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = User.objects.filter(email = username, password = password).first()
        if user == None:
            messages.success(request, f'Error')
            return render(request,'login_system/login.html')
        request.session['role'] = user.role
        if user.role == 'student':
            roleuser = Student.objects.filter(user_userid = user.userid).first()
            courses = StudentEnrollment.objects.filter(student_studentid=roleuser.studentid)
            request.session['id'] = roleuser.studentid
        elif user.role == 'instructor':
            roleuser = Instructor.objects.filter(user_userid=user.userid).first()
            courses = CourseInstructor.objects.filter(instructor_instructorid=roleuser.instructorid)
            request.session['id'] = roleuser.instructorid
        mylist = []
        for course in courses:
            sid = course.coursesection_sectionid.course_courseid.title
            mylist.append(sid)
        return render(request,'login_system/main.html', {'session':request.session, "list" : mylist})
    else:
        form = MyUserCreateForm()
    return render(request,'login_system/login.html', { 'form' : form })

def home(request):
    if request.session['role'] == 'student':
        courses = StudentEnrollment.objects.filter(student_studentid=request.session['id'])
    elif request.session['role'] == 'instructor':
        courses = CourseInstructor.objects.filter(instructor_instructorid=request.session['id'])
    mylist = []
    for course in courses:
        sid = course.coursesection_sectionid.course_courseid.title
        mylist.append(sid)
    return render(request,'login_system/main.html', {'session':request.session, "list" : mylist})



def grade(request):
    return render(request,'login_system/grade.html', {'session':request.session})

def profile(request):
    if request.session['role']=='student':
        user = Student.objects.filter(studentid=request.session['id']).first()
    else:
        user = Instructor.objects.filter(instructorid=request.session['id']).first()
    return render(request,'login_system/profile.html', {'session':request.session, 'user' : user})

def logout(request):
    del request.session['role']
    del request.session['id']
    return redirect('/')
