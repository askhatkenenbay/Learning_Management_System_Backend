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
    return render(request,'adminstudents.html', {'session':request.session, "students" : students})

def instructors(request):
    return render(request,'adminhome.html')

def courses(request):
    return render(request,'adminhome.html')

def create_student(request):
    return render(request,'adminhome.html')

def create_instructor(request):
    return render(request,'adminhome.html')

def create_course(request):
    return render(request,'adminhome.html')

