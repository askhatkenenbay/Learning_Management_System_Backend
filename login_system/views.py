from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from .forms import MyUserCreateForm
from alldata.models import User, School, Department
# this line should not be in master branch
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = User.objects.filter(email = username, password = password).first()
        if user == None:
            messages.success(request, f'Error')
            return render(request,'login_system/login.html')
        return render(request,'login_system/main.html')
    else:
        form = MyUserCreateForm()
    return render(request,'login_system/login.html', { 'form' : form })

def home(request):
    return render(request,'login_system/main.html')

def reg(request):
    if(request.method == 'POST'):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password_copy = request.POST.get('password_copy', None)
        user = User.objects.filter(email = username).first()
        if (password != password_copy or user != None) :
            messages.success(request, f'Error')
            return render(request,'login_system/reg.html')
        school = School.objects.filter(name = "SEDS").first()
        dep = Department.objects.filter(name = "Physics").first()
        temp = User(email=username,password=password, school_name=school, department_name=dep)
        # school_name = SEDS, department_name = Physics
        temp.save()
        messages.success(request, f'Your account has been created! You are now able to log in')
        return render(request,'login_system/login.html')
    return render(request,'login_system/reg.html')

def art(request):
    return render(request,'login_system/art.html')
