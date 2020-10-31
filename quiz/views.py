from django.shortcuts import render

def quizzes(request):
    return render(request,'quizzes.html')

def depression(request):
    return render(request,'depression.html')

def anxiety(request):
    return render(request,'anxiety.html')
