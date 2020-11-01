from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
def quizzes(request):
    return render(request,'quizzes.html')

def depression(request):
    if request.method == 'POST':
        res = 0
        q1 = request.POST.get('q1', None)
        q2 = request.POST.get('q2', None)
        q3 = request.POST.get('q3', None)
        q4 = request.POST.get('q4', None)
        q5 = request.POST.get('q5', None)
        q6 = request.POST.get('q6', None)
        q7 = request.POST.get('q7', None)
        q8 = request.POST.get('q8', None)
        q9 = request.POST.get('q9', None)
        q10 = request.POST.get('q10', None)
        res = deepHelp(q1,res)
        res = deepHelp(q2,res)
        res = deepHelp(q3,res)
        res = deepHelp(q4,res)
        res = deepHelp(q5,res)
        res = deepHelp(q6,res)
        res = deepHelp(q7,res)
        res = deepHelp(q8,res)
        res = deepHelp(q9,res)
        res = deepHelp(q10,res)
        print("-----------------")
        print(res)
        print("-----------------")
        if(res > 20):
            messages.success(request, f'Your answers suggest you are suffering from severe depression. It is important that you schedule an appointment with your doctor or a mental health worker now.') 
        elif(res > 10):
            messages.success(request, f'Your answers suggest you are suffering from moderate depression. Consider watchful waiting, and testing again normally within two weeks. We additionally suggest it would be prudent to start a conversation with your doctor.') 
        elif(res >= 0):
            messages.success(request, f'Your answers suggest you may not be suffering from depression. Still if you feel something isn’t quite right we recommend you schedule an appointment with your doctor.') 
    return render(request,'depression.html')

def deepHelp(value, i):
    if value == "1":
        return i
    elif value == "2":
        return i+1
    elif value == "3":
        return i+2
    elif value == "4":
        return i+3
    return i

def anxiety(request):
    return render(request,'anxiety.html')
