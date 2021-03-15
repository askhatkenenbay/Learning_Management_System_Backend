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
import os
import zipfile
import json
from boto3.session import Session
from io import StringIO
from django.http import HttpResponseRedirect
from django.core.files.storage import default_storage
import shutil
from login_system.forms import *
from shutil import make_archive
from wsgiref.util import FileWrapper
import pdfkit 

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
    student_id = request.session['id']
    student = Student.objects.filter(studentid=student_id).first()
    enrollments = StudentEnrollment.objects.filter(student_studentid=student_id)
    grade_info = []
    for enroll in enrollments:
        # section = Coursesection.objects.filter(sectionid=enroll.coursesection_sectionid).first()
        section = enroll.coursesection_sectionid
        grade = getGrade(student_id, section.sectionid)
        course_name = section.course_courseid.title 
        course_grade = CourseGrades.objects.filter(student_studentid=student_id, coursesection_sectionid=section.sectionid).first()
        temp = GradeInfo(section,grade, course_grade,course_name)
        grade_info.append(temp)
    return render(request,'login_system/grades.html', {'session':request.session,'list':grade_info})

def getGrade(student_id, section_id):
    res = 0
    course_section = Coursesection.objects.filter(sectionid = section_id).first()
    course = course_section.course_courseid
    modules = Coursepagemodule.objects.filter(coursesection_sectionid = course_section.sectionid).order_by('order').all()
    moduleList = []
    for module in modules:
        ass = Assignment.objects.filter(coursepagemodule_moduleid = module).all()
        quiz = Quiz.objects.filter(coursepagemodule_moduleid = module).all()
        for a in ass:
            sub = Assignmentsubmission.objects.filter(assignment_assignmentid = a.assignmentid, student_studentid=student_id).first()
            if(sub == None):
                continue
            res = res + sub.points
        for q in quiz:
            sub = Quizsubmission.objects.filter(quiz_quizid = q.quizid, student_studentid=student_id).first()
            if(sub == None):
                continue
            res = res + sub.points
    return res

class GradeInfo:
    def __init__(self, section, grade, course_grade,name):
        self.section = section
        self.grade = grade
        self.course_grade = course_grade
        self.name = name


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

def mysubmissions(request):
    student = Student.objects.filter(studentid=request.session['id']).first()
    submissions = Assignmentsubmission.objects.filter(student_studentid = student)
    return render(request, 'login_system/mysubmissions.html', {'session': request.session, 'submissions': submissions})

def announcements(request, coursesection_id):
    course_section = Coursesection.objects.filter(sectionid=coursesection_id).first()
    cid = course_section.course_courseid.courseid
    if request.method == 'POST':
        delete = request.POST.get('delete', None)
        if delete is not None:
            id = request.POST.get('annid',None)
            Announcement.objects.filter(announcementid=id).delete()
        else:
            message = request.POST.get('message', None)
            curtime = datetime.datetime.now()
            m = Announcement(text=message, coursesection_sectionid = course_section, date = curtime)
            m.save()
    messages = Announcement.objects.filter(coursesection_sectionid=course_section).order_by('-date')
    return render(request,'login_system/announce.html', {'session':request.session, 'messages': messages,
                                                         'cid': cid, 'sid':coursesection_id})

def assignments(request, coursesection_id):
    course_section = Coursesection.objects.filter(sectionid=coursesection_id).first()
    cid = course_section.course_courseid.courseid
    asses = Assignment.objects.filter(coursepagemodule_moduleid__coursesection_sectionid=course_section)
    return render(request, 'login_system/assignments.html', {'session': request.session, 'asses' : asses,
                                                             'cid': cid, 'sid':coursesection_id })

def assignment(request, coursesection_id, assignment_id):
    if request.method == 'POST':
        studid = request.POST.get('studid', None)
        assid = request.POST.get('assid', None)
        grade = request.POST.get('grade', None)
        feedback = request.POST.get('feedback', None)
        assignment = Assignment.objects.filter(assignmentid=assid).first()
        student = Student.objects.filter(studentid=studid).first()
        sub = Assignmentsubmission.objects.filter(assignment_assignmentid=assignment, student_studentid = student).first()
        sub.points = grade
        sub.feedback = feedback
        sub.save()
    ass = Assignment.objects.filter(assignmentid=assignment_id).first()
    asses = Assignmentsubmission.objects.filter(assignment_assignmentid=ass)
    return render(request, 'login_system/assignment.html', {'session': request.session, 'asses' : asses,
                                                             'sid' : coursesection_id, 'assignment' : ass })

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

def cexam(request):
    if request.method=='POST':
        print(request.POST.get('section_id', None))
        form=QuizCreateForm(request.POST, request.POST.get('section_id', None))
        if form.is_valid():
            print("YEEEEE")
            temp = Quiz(coursepagemodule_moduleid=form['module'],name=form['name'])
            temp.save()
            return HttpResponse('success')
        else:
            print("NOOOOOO")

    print("#1")
    return render(request, 'login_system/exam/cexam.html') 

def quiz(request):
    print("QUIZ STARTED")
    return render(request, 'login_system/exam/quizMulti.html')

def course(request, course_id, coursesection_id):
    if request.method == 'POST':
        if request.POST.get('quizStart') == "quizStart":
            print("QUIZ STARTEDs")
            return redirect('/quiz')
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
        print(content)
        print("<--")
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
            #
            q_and = request.POST.getlist('q-ans')
            questions = request.POST.getlist('q')
            index = 0
            for ans in q_and:
                ans_question = Quizquestion(quiz_quizid=q, text = ans, points = 1, is_ans = True).save()
                for x in range(3):
                    Quizquestion(quiz_quizid=q, text = x, points = 1, friend = ans_question.questionid).save()

            # 
            return HttpResponseRedirect(request.path_info)
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
    if request.GET.get('download') == "download":
        download_files(modules,request.session['id'])
        dirName = str(request.session['id'])+"-downloads"
        listFiles = os.listdir('./'+dirName)
        res = zipMe(listFiles,request.session['id'])
        shutil.rmtree(dirName, ignore_errors=True)
        os.remove(dirName+".zip")
        return res


        
    moduleList = []
    for module in modules:
        ass = Assignment.objects.filter(coursepagemodule_moduleid = module).all()
        quiz = Quiz.objects.filter(coursepagemodule_moduleid = module).all()
        myFile = File.objects.filter(coursepagemodule_moduleid = module).all()
        temp = ModuleInfo(module,ass,quiz,myFile)
        moduleList.append(temp)
    return render(request,'login_system/coursepage.html', {'session':request.session, 'course':course, 'course_section':course_section, 'modules':modules, 'list':moduleList})

def zipMe(listFiles, mid):
    files_path = './'+ str(mid)+"-downloads"
    print(files_path)
    path_to_zip = make_archive(files_path, "zip", files_path)
    response = HttpResponse(FileWrapper(open(path_to_zip,'rb')), content_type='application/zip')
    file_name = 'course_content'
    response['Content-Disposition'] = 'attachment; filename="{filename}.zip"'.format(
        filename = file_name.replace(" ", "_")
    )
    return response

def download_files(modules,mid):
    f = open('/etc/config.json',)
    data = json.load(f)	
    session = Session(aws_access_key_id=data["AWS_ACCESS_KEY_ID"],aws_secret_access_key=data["AWS_SECRET_ACCESS_KEY"])
    s3 = session.resource('s3')
    bucket = data["AWS_STORAGE_BUCKET_NAME"]
    my_bucket = s3.Bucket(bucket)
    os.mkdir(os.path.join('./', str(mid)+"-downloads"))
    for module in modules:
        files = File.objects.filter(coursepagemodule_moduleid = module).all()
        for cfile in files:
            my_bucket.download_file(str(cfile.myFile),'./'+str(mid)+'-downloads/'+str(cfile.myFile))

def documents(request):
    documents = School.objects.all()
    if request.method == 'POST':
        post_id = request.POST.get('post_id', None)
        if post_id == 'schedule':
            school = request.POST.get('school', None)
            url = request.get_host() + '/semester-courses/' + school + '/'
            pdf = pdfkit.from_url(url, False)
            response = HttpResponse(pdf,content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="school_schedule_by_term.pdf"'
            return response
        elif post_id == 'requirements':
            school = request.POST.get('school', None)
            url = request.get_host() + '/requirements-courses/' + school + '/'
            pdf = pdfkit.from_url(url, False)
            response = HttpResponse(pdf,content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="course_list_with_requirements.pdf"'
            return response
    return render(request, 'login_system/documents.html', {'session':request.session, 'documents':documents, 'semester':semester, 'year':year})

def semester_courses(request, school):
    sections = list(Coursesection.objects.filter(semester=semester, year=year))
    res_sections = []
    days_dic = {'1':'Mn', '2':'Tu', '3':'Wn', '4':'Th', '5':'Fr', '6':'St'}
    for sec in sections:
        if sec.course_courseid.department_name.school_name.name == school:
            enrolled = StudentEnrollment.objects.filter(coursesection_sectionid=sec.sectionid).count()
            days = list(Sectionday.objects.filter(coursesection_sectionid=sec.sectionid).all())
            for i, day in enumerate(days):
                days[i] = days_dic[day.day]
            days = ','.join(days)
            instructors = list(CourseInstructor.objects.filter(coursesection_sectionid=sec.sectionid).all())
            for i, ins in enumerate(instructors):
                instructors[i] = ins.instructor_instructorid.user_userid.first_name + ' ' + ins.instructor_instructorid.user_userid.last_name
            instructors = ', '.join(instructors)
            res_sections.append([sec, enrolled, days, instructors])
    date = str(datetime.datetime.now())[:19]
    school = School.objects.filter(name=school).first()
    return render(request, 'login_system/semestercourses.html', {"sections":res_sections, 'semester':semester, 'year':year, 'date':date, 'school':school})

def requirements_courses(request, school):
    courses = list(Course.objects.all())
    res_courses = []
    for course in courses:
        sections = list(Coursesection.objects.filter(course_courseid = course.courseid, semester = semester, year = year))
        if len(sections) != 0 and course.department_name.school_name.name == school:
            priotity_1, priotity_2, priotity_3 = [], [], []
            priorities = list(Priority.objects.filter(course_courseid=course.courseid).all())
            for i, p in enumerate(priorities):
                if p.type == 1:
                    priotity_1.append(p.department_name.name + ', ' + str(p.year) + ' Year Students')
                elif p.type == 2:
                    priotity_2.append(p.department_name.name + ', ' + str(p.year) + ' Year Students')
                else:
                    priotity_3.append(p.department_name.name + ', ' + str(p.year) + ' Year Students')
            requisites = list(Requisite.objects.filter(course_courseid=course.courseid).all())
            for i, req in enumerate(requisites):
                if req.is_optional:
                    requisites[i] = req.type + ': ' + req.req_course_courseid.course_code + ' ' + req.req_course_courseid.title + ', optional'
                else:
                    requisites[i] = req.type + ': ' + req.req_course_courseid.course_code + ' ' + req.req_course_courseid.title + ', required'
            res_courses.append([course, priotity_1, priotity_2, priotity_3, requisites])

    school = School.objects.filter(name=school).first()
    return render(request, 'login_system/requirementscourses.html', {"courses":res_courses, 'semester':semester, 'year':year, 'school':school})

def search(req, reg_cors, prior_cors):
    school = req.POST.get('school', None)
    department = req.POST.get('department', None)
    instructor = req.POST.get('instructor', None)
    course_title = req.POST.get('course_title', None)
    course_code = req.POST.get('course_code', None)
    show_registered = req.POST.get('show_registered', None)
    show_priority = req.POST.get('show_priority', None)
    show_all = req.POST.get('show_all', None)
    courses = []
    filters = [school, department, instructor, course_title, course_code, show_registered, show_priority, show_all]

    if show_all == 'on':
        courses = Course.objects.all()
    elif show_registered == 'on':
        courses = reg_cors
    elif show_priority == 'on':
        courses = prior_cors
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
    return filter_course(courses), filters

def filter_course(courses):
    courses = list(courses)
    res_courses = []
    for course in courses:
        sections = list(Coursesection.objects.filter(course_courseid = course.courseid,
                                                semester = semester,
                                                year = year))
        if len(sections) != 0:
            res_courses.append(course)
    return res_courses

def get_courses_of_proirity(student):
    registrationdate = Registrationdate.objects.filter(year=student.year_of_study, open_time__lte = datetime.datetime.now()).order_by('-priority').first()
    cur_priority = registrationdate.priority
    user = User.objects.filter(userid = student.user_userid.userid).first()
    dep = Department.objects.filter(name = user.department_name.name).first()
    courses_of_proirity = list(Priority.objects.filter(type__lte=cur_priority, year=student.year_of_study, department_name = dep.name).all())
    for i, c in enumerate(courses_of_proirity):
        courses_of_proirity[i] = c.course_courseid
    return courses_of_proirity

def get_busy_time(sections_enrolled):
    busy_time = []
    for pair in sections_enrolled:
        sec = Coursesection.objects.filter(sectionid=pair.coursesection_sectionid.sectionid).first()
        days = list(Sectionday.objects.filter(coursesection_sectionid = sec.sectionid).all())
        for d in days:
            busy_time.append((d.day, sec.start_time, sec.end_time))
    return busy_time


def registration(request):
    student = Student.objects.filter(studentid = request.session['id']).first()
    sections_enrolled = list(StudentEnrollment.objects.filter(student_studentid=request.session['id'],
                                                   coursesection_sectionid__year=year,
                                                   coursesection_sectionid__semester=semester))
    courses_registered = []
    les = [[None for x in range(6)] for y in range(12)]
    for course in sections_enrolled:
        sec = Coursesection.objects.filter(sectionid=course.coursesection_sectionid.sectionid).first()
        courses_registered.append(Course.objects.filter(courseid = sec.course_courseid.courseid).first())
        sid = course.coursesection_sectionid
        i = sid.start_time.hour - 8
        days = Sectionday.objects.filter(coursesection_sectionid = sid)
        for day in days:
            j = int(day.day)-1
            les[i][j] = sid
    
    courses_of_proirity = get_courses_of_proirity(student)

    if request.method == 'POST':
        post_id = request.POST.get('post_id', None)
        if post_id == 'search':
            courses, filters = search(request, courses_registered, courses_of_proirity)
            return render(request, 'login_system/registration.html', {'session':request.session, 'les':les, 'courses':courses, 'filters':filters, 'isChosen':False})

        elif post_id == 'choose':
            busy_time = get_busy_time(sections_enrolled)
            sections_time = []
            courses, filters = search(request, courses_registered, courses_of_proirity)
            chosen_course = request.POST.get('chosen_course', None)
            chosen_course = Course.objects.filter(courseid = chosen_course).first()
            course_sections = list(Coursesection.objects.filter(course_courseid = chosen_course.courseid).all())
            sections_days = []
            days_dic = {'1':'Mn', '2':'Tu', '3':'Wn', '4':'Th', '5':'Fr', '6':'St'}
            sections_L, sections_S, sections_R, sections_Lab = [],[],[],[]
            for s in course_sections:
                section_time = []
                ds = list(Sectionday.objects.filter(coursesection_sectionid = s.sectionid).all())
                for i, d in enumerate(ds):
                    section_time.append((d.day, s.start_time, s.end_time))
                    ds[i] = days_dic[d.day]
                ds = ' '.join(ds)
                sections_days.append(ds)
                sections_time.append(section_time)

            for i, s in enumerate(course_sections):
                isFull = False
                capacity = s.capacity
                taken_places = StudentEnrollment.objects.filter(coursesection_sectionid = s.sectionid).count()
                cap = str(taken_places)+'/'+str(capacity)
                if taken_places >= capacity:
                    isFull = True
                isOverlap = False
                for t in sections_time[i]:
                    if isOverlap:
                        break
                    for j in busy_time:
                        if j[0] == t[0]:
                            if j[1] == t[1] or j[2] == t[2]:
                                isOverlap = True
                                course_sections[i] = [s, sections_days[i], isOverlap]
                                break
                            elif j[1] > t[1] and t[2] > j[2]:
                                isOverlap = True
                                course_sections[i] = [s, sections_days[i], isOverlap]
                                break
                            elif j[1] < t[1] and j[1] > t[2]:
                                isOverlap = True
                                course_sections[i] = [s, sections_days[i], isOverlap]
                                break
                            elif j[1] > t[1] and t[1] > j[2]:
                                isOverlap = True
                                course_sections[i] = [s, sections_days[i], isOverlap]
                                break
                if s.section_type == 'Lecture':
                    sections_L.append([s, sections_days[i], isOverlap, isFull, cap])
                elif s.section_type == 'Seminar':
                    sections_S.append([s, sections_days[i], isOverlap, isFull, cap])
                elif s.section_type == 'Recitation':
                    sections_R.append([s, sections_days[i], isOverlap, isFull, cap])
                else:
                    sections_Lab.append([s, sections_days[i], isOverlap, isFull, cap])

            isOverlap_L, isOverlap_S, isOverlap_R, isOverlap_Lab = False, False, False, False
            isFull_L, isFull_S, isFull_R, isFull_Lab = False, False, False, False
            if sections_L:
                isOverlap_L = True
                isFull_L = True
                for course_section in sections_L:
                    if course_section[2] == False:
                        isOverlap_L = False
                        break
                for course_section in sections_L:
                    if course_section[3] == False:
                        isFull_L = False
                        break

            if sections_S:
                isOverlap_S = True
                isFull_S = True
                for course_section in sections_S:
                    if course_section[2] == False:
                        isOverlap_S = False
                        break
                for course_section in sections_S:
                    if course_section[3] == False:
                        isFull_S = False
                        break

            if sections_R:
                isOverlap_R = True
                isFull_R = True
                for course_section in sections_R:
                    if course_section[2] == False:
                        isOverlap_R = False
                        break
                for course_section in sections_R:
                    if course_section[3] == False:
                        isFull_R = False
                        break

            if sections_Lab:
                isOverlap_Lab = True
                isFull_Lab = True
                for course_section in sections_Lab:
                    if course_section[2] == False:
                        isOverlap_Lab = False
                        break
                for course_section in sections_Lab:
                    if course_section[3] == False:
                        isFull_Lab = False
                        break

            isOverlap = isOverlap_L or  isOverlap_S or isOverlap_R or isOverlap_Lab
            isFull = isFull_L or  isFull_S or isFull_R or isFull_Lab

            # isPriority = (chosen_course in courses_of_proirity)
            isPriority = True
            isRegistered = (chosen_course in courses_registered)
            return render(request, 'login_system/registration.html', {'session':request.session, 'les':les, 'courses':courses, 'filters':filters, 'isChosen':True, 
                                                                    'chosen_course':chosen_course, 'sections_L':sections_L, 'sections_S':sections_S,'sections_R':sections_R,
                                                                    'sections_Lab':sections_Lab,'isRegistered':isRegistered, 'isPriority':isPriority,'isOverlap':isOverlap, 'isFull':isFull})

        elif post_id == 'register':
            courses, filters = search(request, courses_registered, courses_of_proirity)
            chosen_sections = []            
            chosen_sections.append(request.POST.get('chosen_section_L', None))
            chosen_sections.append(request.POST.get('chosen_section_R', None))
            chosen_sections.append(request.POST.get('chosen_section_S', None))
            chosen_sections.append(request.POST.get('chosen_section_Lab', None))
            for sec in chosen_sections:
                if sec != None:
                    chosen_section = Coursesection.objects.filter(sectionid = sec).first()
                    studentenrollment = StudentEnrollment()
                    studentenrollment.student_studentid = student
                    studentenrollment.coursesection_sectionid = chosen_section
                    studentenrollment.save()

            sections_enrolled = list(StudentEnrollment.objects.filter(student_studentid=request.session['id'],
                                                   coursesection_sectionid__year=year,
                                                   coursesection_sectionid__semester=semester))
            courses_registered = []
            les = [[None for x in range(6)] for y in range(12)]
            for course in sections_enrolled:
                sec = Coursesection.objects.filter(sectionid=course.coursesection_sectionid.sectionid).first()
                courses_registered.append(Course.objects.filter(courseid = sec.course_courseid.courseid).first())
                sid = course.coursesection_sectionid
                i = sid.start_time.hour - 8
                days = Sectionday.objects.filter(coursesection_sectionid = sid)
                for day in days:
                    j = int(day.day)-1
                    les[i][j] = sid
            return render(request, 'login_system/registration.html', {'session':request.session, 'les':les, 'courses':courses, 'filters':filters, 'isChosen':False})

        elif post_id == 'drop':
            courses, filters = search(request, courses_registered, courses_of_proirity)
            chosen_course = request.POST.get('chosen_course', None)
            chosen_course = Course.objects.filter(courseid = chosen_course).first()
            sections = list(Coursesection.objects.filter(course_courseid = chosen_course.courseid).all())
            for sec in sections:
                StudentEnrollment.objects.filter(student_studentid = student.studentid, coursesection_sectionid = sec.sectionid).delete()

            sections_enrolled = list(StudentEnrollment.objects.filter(student_studentid=request.session['id'],
                                                   coursesection_sectionid__year=year,
                                                   coursesection_sectionid__semester=semester))
            courses_registered = []
            les = [[None for x in range(6)] for y in range(12)]
            for course in sections_enrolled:
                sec = Coursesection.objects.filter(sectionid=course.coursesection_sectionid.sectionid).first()
                courses_registered.append(Course.objects.filter(courseid = sec.course_courseid.courseid).first())
                sid = course.coursesection_sectionid
                i = sid.start_time.hour - 8
                days = Sectionday.objects.filter(coursesection_sectionid = sid)
                for day in days:
                    j = int(day.day)-1
                    les[i][j] = sid
            return render(request, 'login_system/registration.html', {'session':request.session, 'les':les, 'courses':courses, 'filters':filters, 'isChosen':False})

    courses = []
    filters = ['','','','','','off','off','off']
    return render(request, 'login_system/registration.html', {'session':request.session, 'les':les, 'courses':courses, 'filters':filters, 'isChosen':False})

