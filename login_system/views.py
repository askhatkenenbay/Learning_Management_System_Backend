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
#now = datetime.datetime.now()
#year = now.year
#semester = ms[now.month]
year = 2020
semester = "Fall"

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
        if user.role == 'admin':
            request.session['id'] = user.userid
            return redirect('/administrator/home')
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
        courses = StudentEnrollment.objects.filter(student_studentid=request.session['id'],
                                                   coursesection_sectionid__year=year,
                                                   coursesection_sectionid__semester=semester)
    elif request.session['role'] == 'instructor':
        courses = CourseInstructor.objects.filter(instructor_instructorid=request.session['id'],
                                                  coursesection_sectionid__year=year,
                                                  coursesection_sectionid__semester=semester)
    mylist = []
    for course in courses:
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

def advisee(request, student_id):
    schedule = request.POST.get('schedule', None)
    student = Student.objects.filter(studentid=student_id).first()
    if schedule == "lock":
        student.schedule_lock = True
        student.save()
    elif schedule == "unlock":
        student.schedule_lock = False
        student.save()
    elif schedule == "approve":
        student.schedule_approve = True
        student.save()
    elif schedule == "unapprove":
        student.schedule_approve = False
        student.save()
    courses = StudentEnrollment.objects.filter(student_studentid=student_id,
                                               coursesection_sectionid__year=year,
                                               coursesection_sectionid__semester=semester)
    les = [[None for x in range(6)] for y in range(12)]
    for course in courses:
        sid = course.coursesection_sectionid
        i = sid.start_time.hour - 8
        days = Sectionday.objects.filter(coursesection_sectionid=sid)
        for day in days:
            j = int(day.day) - 1
            les[i][j] = sid
    return render(request, 'login_system/advisee.html',{'session': request.session, 'user' : student, "les" : les })

def schedule(request):
    locked = False
    approved = False
    if request.session['role'] == 'student':
        courses = StudentEnrollment.objects.filter(student_studentid=request.session['id'],
                                                   coursesection_sectionid__year=year,
                                                   coursesection_sectionid__semester=semester)
        student = Student.objects.filter(studentid=request.session['id']).first()
        locked = student.schedule_lock
        approved = student.schedule_approve
    elif request.session['role'] == 'instructor':
        courses = CourseInstructor.objects.filter(instructor_instructorid=request.session['id'],
                                                  coursesection_sectionid__year=year,
                                                  coursesection_sectionid__semester=semester)
    les = [[None for x in range(6)] for y in range(12)]
    for course in courses:
        sid = course.coursesection_sectionid
        i = sid.start_time.hour - 8
        days = Sectionday.objects.filter(coursesection_sectionid = sid)
        for day in days:
            j = int(day.day)-1
            les[i][j] = sid
    return render(request, 'login_system/schedule.html', {'session':request.session, "les" : les,
                                                          "locked" : locked, "approved" : approved})

def profile(request):
    if request.session['role']=='student':
        user = Student.objects.filter(studentid=request.session['id']).first()
    else:
        user = Instructor.objects.filter(instructorid=request.session['id']).first()
    return render(request,'login_system/profile.html', {'session':request.session, 'user' : user})

def announcements(request, coursesection_id):
    course_section = Coursesection.objects.filter(sectionid=coursesection_id).first()
    cid = course_section.course_courseid.courseid
    if request.method == 'POST':
        message = request.POST.get('message', None)
        curtime = datetime.datetime.now()
        m = Announcement(text=message, coursesection_sectionid = course_section, date = curtime)
        m.save()
    messages = Announcement.objects.filter(coursesection_sectionid=course_section)
    return render(request,'login_system/announce.html', {'session':request.session, 'messages': messages, 'cid': cid, 'sid':coursesection_id})

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
            submission.myFile = request.FILES['filename']
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
            filename = request.FILES['filename']
            qqq = File(description = desc, coursepagemodule_moduleid = module, myFile=filename)
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

def search(req):
    school = req.POST.get('school', None)
    department = req.POST.get('department', None)
    instructor = req.POST.get('instructor', None)
    course_title = req.POST.get('course_title', None)
    course_code = req.POST.get('course_code', None)
    show_available = req.POST.get('show_available', None)
    show_priority = req.POST.get('show_priority', None)
    show_all = req.POST.get('show_all', None)
    courses = []
    filters = [school, department, instructor, course_title, course_code, show_available, show_priority, show_all]

    if show_all == 'on':
        courses = Course.objects.all()
    elif course_title != '' and course_code != '':
        courses = Course.objects.filter(title = course_title, course_code = course_code).all()
    elif course_title != '':
        courses = Course.objects.filter(title = course_title).all()
    elif course_code != '':
        courses = Course.objects.filter(course_code = course_code).all()
    elif instructor != '':
        first_name, last_name = instructor.split()
        user = User.objects.filter(first_name = first_name, last_name = last_name).first()
        if user == None:
            courses = []
        else:
            instructor_id = Instructor.objects.filter(user_user = user.user_userid).first()
            course_instrs = CourseInstructor.objects.filter(instructor_instructorid = instructor_id).all()
            for course_instr in course_instrs:
                course_section = Coursesection.objects.filter(course_courseid = course_instr.coursesection_sectionid).first()
                courses.append(Course.objects.filter(courseid = course_section.course_courseid).first())
            courses = list(set(courses))
    elif department != '':
        courses = Course.objects.filter(department_name = department).all()
    elif school != '':
        departments = Department.objects.filter(school_name = school).all()
        courses = []
        for dep in departments:
            courses_of_dep = Course.objects.filter(department_name = dep.name).all()
            for c in courses_of_dep:
                courses.append(c)
    return courses, filters

def registration(request):
    student = Student.objects.filter(studentid = request.session['id']).first()

    if request.method == 'POST':
        post_id = request.POST.get('post_id', None)
        if post_id == 'search':
            courses, filters = search(request)
            return render(request, 'login_system/registration.html', {'session':request.session, 'courses':courses, 'filters':filters, 'isChosen':False})

        elif post_id == 'choose':
            courses, filters = search(request)
            chosen_course = request.POST.get('chosen_course', None)
            chosen_course = Course.objects.filter(courseid = chosen_course).first()
            course_sections = Coursesection.objects.filter(course_courseid = chosen_course.courseid).all()
            return render(request, 'login_system/registration.html', {'session':request.session, 'courses':courses, 'filters':filters, 'isChosen':True, 'chosen_course':chosen_course, 'course_sections':course_sections})

        elif post_id == 'register':
            courses, filters = search(request)
            print('REGISTER')
            chosen_course = request.POST.get('chosen_course', None)
            chosen_course = Course.objects.filter(courseid = chosen_course).first()
            chosen_section = request.POST.get('chosen_section', None)
            chosen_section = Coursesection.objects.filter(sectionid = chosen_section).first()
            course_sections = Coursesection.objects.filter(course_courseid = chosen_course.courseid).all()
            studentenrollment = StudentEnrollment()
            studentenrollment.student_studentid = student
            studentenrollment.coursesection_sectionid = chosen_section
            studentenrollment.save()
            return render(request, 'login_system/registration.html', {'session':request.session, 'courses':courses, 'filters':filters, 'isChosen':True, 'chosen_course':chosen_course, 'course_sections':course_sections})

    courses = []
    filters = ['','','','','','off','off','off']
    return render(request, 'login_system/registration.html', {'session':request.session, 'courses':courses, 'filters':filters, 'isChosen':False})
