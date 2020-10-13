from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(username)
        print(password)
        return render(request,'login_system/home.html')
    return render(request,'login_system/login.html')

def home(request):
    return render(request,'login_system/home.html')
