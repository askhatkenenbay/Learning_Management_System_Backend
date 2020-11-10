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

def schedule(request):
    if request.session['role'] == 'student':
        courses = StudentEnrollment.objects.filter(student_studentid=request.session['id'], coursesection_sectionid__year=year, coursesection_sectionid__semester=semester)
    elif request.session['role'] == 'instructor':
        courses = CourseInstructor.objects.filter(instructor_instructorid=request.session['id'],  coursesection_sectionid__year=year, coursesection_sectionid__semester=semester)
    les = [[None for x in range(6)] for y in range(12)]
    dd = {"M": 0, "T": 1, "W": 2, "R": 3, "F": 4, "S": 5}
    for course in courses:
        sid = course.coursesection_sectionid
        i = sid.start_time.hour - 8
        days = Sectionday.objects.filter(coursesection_sectionid = sid)
        for day in days:
            d = day.day
            j = dd[d]
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
    return redirect('/')

def participants(request, coursesection_id):
    student, prof = getListOfParticipants(coursesection_id)
    part = {
        "students" : student,
        "profs" : prof
    }
    return render(request,'login_system/participants.html', {'list':part})

def getListOfParticipants(id):
    section = Coursesection.objects.filter(sectionid=id).first()
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
    return studentList, profList

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

def course(request, course_id, coursesection_id):
    course_section = Coursesection.objects.filter(sectionid = coursesection_id).first()
    course = course_section.course_courseid
    modules = Coursepagemodule.objects.filter(coursesection_sectionid = coursesection_id).all()
    return render(request,'login_system/coursepage.html', {'session':request.session, 'course':course, 'course_section':course_section, 'modules':modules})