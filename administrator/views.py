from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect

def home(request):
    return render(request,'index.html')
