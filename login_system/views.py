from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from .forms import MyUserCreateForm
from alldata.models import User, School, Department, Student,StudentEnrollment,Coursesection,Course
from django.contrib.auth.decorators import login_required, user_passes_test

student_required = user_passes_test(lambda user: user.role == 'student', login_url='/')
def student_required(view_func):
    decorated_view_func = login_required(student_required(view_func))
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
        student = Student.objects.filter(user_userid = user.userid).first()
        courses = StudentEnrollment.objects.filter(student_studentid = student.studentid)
        mylist = []
        for course in courses:
            sid = course.coursesection_sectionid.course_courseid.title
            mylist.append(sid)
        return render(request,'login_system/main.html', {'session':request.session, "list" : mylist})
    else:
        form = MyUserCreateForm()
    return render(request,'login_system/login.html', { 'form' : form })

def home(request):
    return render(request,'login_system/main.html')



def grade(request):
    return render(request,'login_system/grade.html')
