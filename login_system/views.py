from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from .forms import MyUserCreateForm
from alldata.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.http import HttpResponseRedirect
noadmin_required = user_passes_test(lambda user: user.role == 'student' or user.role == 'instructor', login_url='/')
def noadmin_required(view_func):
    decorated_view_func = login_required(noadmin_required(view_func))
    return decorated_view_func

ms = {1: "Spring", 2: "Spring",3: "Spring",4: "Spring",5: "Spring",
      6: "Summer",7: "Summer",8: "Fall",9: "Fall",10: "Fall",11: "Fall",12: "Fall"}
now = datetime.datetime.now()
year = now.year
semester = ms[now.month]

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = User.objects.filter(email = username, password = password).first()
        if user == None:
            messages.success(request, f'Error')
            return render(request,'login_system/login.html')
        request.session['role'] = user.role
        request.session['name'] = user.first_name
        request.session['surname'] = user.last_name
        if user.role == 'student':
            roleuser = Student.objects.filter(user_userid = user.userid).first()
            request.session['id'] = roleuser.studentid
        elif user.role == 'instructor':
            roleuser = Instructor.objects.filter(user_userid=user.userid).first()
            request.session['id'] = roleuser.instructorid
        return redirect('/home')
    else:
        form = MyUserCreateForm()
    return render(request,'login_system/login.html', { 'form' : form })

def home(request):
    if request.session['role'] == 'student':
        courses = StudentEnrollment.objects.filter(student_studentid=request.session['id'],  coursesection_sectionid__year=year, coursesection_sectionid__semester=semester)
    elif request.session['role'] == 'instructor':
        courses = CourseInstructor.objects.filter(instructor_instructorid=request.session['id'],  coursesection_sectionid__year=year, coursesection_sectionid__semester=semester)
    mylist = []
    for course in courses:
        #sid = (course.coursesection_sectionid.course_courseid.title, course.coursesection_sectionid.course_courseid.courseid, course.coursesection_sectionid.sectionid)
        sid = course.coursesection_sectionid
        mylist.append(sid)
    return render(request,'login_system/main.html', {'session':request.session, "list" : mylist})


def grades(request):
    return render(request,'login_system/grades.html', {'session':request.session})

def adviseeList(request):
    advisees = Advice.objects.filter(instructor_instructorid=request.session['id'])
    list = []
    for advisee in advisees:
        advid = advisee.student_studentid
        list.append(advid)
    return render(request,'login_system/adviseeList.html', {'session':request.session, "list" : list})

def schedule(request):
    if request.session['role'] == 'student':
        courses = StudentEnrollment.objects.filter(student_studentid=request.session['id'], coursesection_sectionid__year=year, coursesection_sectionid__semester=semester)
    elif request.session['role'] == 'instructor':
        courses = CourseInstructor.objects.filter(instructor_instructorid=request.session['id'],  coursesection_sectionid__year=year, coursesection_sectionid__semester=semester)
    les = [[None for x in range(6)] for y in range(12)]
    for course in courses:
        sid = course.coursesection_sectionid
        i = sid.start_time.hour - 8
        days = Sectionday.objects.filter(coursesection_sectionid = sid)
        for day in days:
            j = int(day.day)-1
            les[i][j] = sid
    return render(request, 'login_system/schedule.html', {'session':request.session, "les" : les})

def profile(request):
    if request.session['role']=='student':
        user = Student.objects.filter(studentid=request.session['id']).first()
    else:
        user = Instructor.objects.filter(instructorid=request.session['id']).first()
    return render(request,'login_system/profile.html', {'session':request.session, 'user' : user})

def logout(request):
    del request.session['role']
    del request.session['id']
    del request.session['name']
    del request.session['surname']
    return redirect('/')

def participants(request, coursesection_id):
    student, prof,title, level = getListOfParticipants(coursesection_id)
    part = {
        "students" : student,
        "profs" : prof,
        "title" : title,
        "level" : level
    }
    return render(request,'login_system/participants.html', {'session':request.session, 'list':part})

def getListOfParticipants(id):
    section = Coursesection.objects.filter(sectionid=id).first()
    title = section.course_courseid.title
    level = section.course_courseid.course_code
    students = StudentEnrollment.objects.filter(coursesection_sectionid = section)
    profs = CourseInstructor.objects.filter(coursesection_sectionid = section)
    studentList = []
    profList = []
    for student in students:
        user = student.student_studentid.user_userid
        fname = user.first_name
        sname = user.last_name
        dep = user.department_name
        department = dep.name
        school = dep.school_name.name
        year = student.student_studentid.year_of_study
        s1 = StudentInfo(fname, sname, department, school, year)
        studentList.append(s1)
    for prof in profs:
        temp = prof.instructor_instructorid
        position = temp.position
        user = temp.user_userid
        fname = user.first_name
        sname = user.last_name
        dep = user.department_name
        department = dep.name
        school = dep.school_name.name
        p1 = ProfInfo(fname,sname,department,school,position)
        profList.append(p1)
    return studentList, profList,title,level

class StudentInfo:
  def __init__(self, fname, sname, department, school, year):
    self.fname = fname
    self.sname = sname
    self.department = department
    self.school = school
    self.year = year 

class ProfInfo:
  def __init__(self, fname, sname, department, school, position):
    self.fname = fname
    self.sname = sname
    self.department = department
    self.school = school
    self.position = position

class ModuleInfo:
  def __init__(self, cModule, ass, quiz, myFile):
    self.cModule = cModule
    self.ass = ass
    self.quiz = quiz
    self.myFile = myFile

def course(request, course_id, coursesection_id):
    if request.method == 'POST':
        sua = request.POST.get('student-upload-ass', None)
        if sua is not None:
            submission = Assignmentsubmission()
            submission.date = datetime.datetime.now()
            submission.myFile = request.POST.get('filename', None)
            ass = Assignment.objects.filter(assignmentid = request.POST.get('assID', None)).first()
            submission.assignment_assignmentid = ass
            student = Student.objects.filter(studentid = request.session['id']).first()
            submission.student_studentid = student
            submission.points = 0
            submission.save()
            print("NEW SUBMISSION")
            # return HttpResponseRedirect(request.path_info)
        content = request.POST.get('new-content', None)
        if content == "quiz":
            print("NEW QUIZ ADDED")
            name = request.POST.get('title', None)
            desc = request.POST.get('desc', None)
            startDate = request.POST.get('startDate', None)
            startTime = request.POST.get('startTime', None)
            start = str(startDate) + " " +  str(startTime)
            endDate = request.POST.get('endDate', None)
            endTime = request.POST.get('endTime', None)
            end = str(endDate) + " "+ str(endTime)
            maxPoint = request.POST.get('maxPoint', None)
            limit = request.POST.get('limit', None)
            moduleId = request.POST.get('moduleID', None)
            module = Coursepagemodule.objects.filter(moduleid = moduleId).first()
            q = Quiz(name = name, description = desc, open_time = start, close_time = end, time_limit = limit, max_point = maxPoint,coursepagemodule_moduleid = module)
            q.save()
            # return HttpResponseRedirect(request.path_info)
        elif content == "ass":
            print("NEW ASS ADDED")
            name = request.POST.get('name', None)
            desc = request.POST.get('description', None)
            startDate = request.POST.get('startDate', None)
            startTime = request.POST.get('startTime', None)
            start = str(startDate) + " " +  str(startTime)
            endDate = request.POST.get('endDate', None)
            endTime = request.POST.get('endTime', None)
            end = str(endDate) + " "+ str(endTime)
            maxPoint = request.POST.get('maxPoint', None)
            moduleId = request.POST.get('moduleID', None)
            module = Coursepagemodule.objects.filter(moduleid = moduleId).first()
            a = Assignment(name = name, description = desc,start_date = start, due_date = end, max_point = maxPoint,coursepagemodule_moduleid = module)
            a.save()
            # return HttpResponseRedirect(request.path_info)
        elif content == "myFile":
            print("NEW File ADDED")
            desc = request.POST.get('desc', None)
            # tempFile = request.FILES['filename']
            moduleId = request.POST.get('moduleID', None)
            module = Coursepagemodule.objects.filter(moduleid = moduleId).first()
            qqq = File(description = desc, coursepagemodule_moduleid = module)
            qqq.myFile = request.POST.get('filename', None)
            qqq.save()
            # return HttpResponseRedirect(request.path_info)
        elif content == "content":
            name = request.POST.get('name', None)
            order = request.POST.get('order', None)
            sectionID = request.POST.get('section', None) 
            section = Coursesection.objects.filter(sectionid = sectionID).first()
            temp = Coursepagemodule(coursesection_sectionid = section, title = name, order = order)
            temp.save()
            print("NEW MODULE")
            # return HttpResponseRedirect(request.path_info)

        delete = request.POST.get('delete', None)
        
        if delete == "quiz":
            myID = request.POST.get('quizID', None)
            Quiz.objects.filter(quizid = myID).delete()
        elif delete == "ass":
            myID = request.POST.get('assID', None)
            Assignment.objects.filter(assignmentid = myID).delete()
        elif delete == "file":
            myID = request.POST.get('fileID', None)
            File.objects.filter(fileid = myID).delete()
        elif delete == "module":
            myID = request.POST.get('moduleID', None)
            Coursepagemodule.objects.filter(moduleid = myID).delete()
    

    course_section = Coursesection.objects.filter(sectionid = coursesection_id).first()
    course = course_section.course_courseid
    modules = Coursepagemodule.objects.filter(coursesection_sectionid = coursesection_id).order_by('order').all()
    moduleList = []
    for module in modules:
        ass = Assignment.objects.filter(coursepagemodule_moduleid = module).all()
        quiz = Quiz.objects.filter(coursepagemodule_moduleid = module).all()
        myFile = File.objects.filter(coursepagemodule_moduleid = module).all()
        temp = ModuleInfo(module,ass,quiz,myFile)
        moduleList.append(temp)
    return render(request,'login_system/coursepage.html', {'session':request.session, 'course':course, 'course_section':course_section, 'modules':modules, 'list':moduleList})

def download(request, file_id):
    print(file_id)
    temp = File.objects.filter(fileid = file_id).first()
    data = temp.myFile.read()
    return data
    # response = HttpResponse(temp.myFile.read())
    # print("HERE")
    # return response