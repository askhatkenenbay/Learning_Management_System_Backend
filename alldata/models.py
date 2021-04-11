from django.db import models

class School(models.Model):
    name = models.CharField(primary_key=True, max_length=45)
    full_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'school'
        unique_together = (('name'),)


class Department(models.Model):
    name = models.CharField(primary_key=True, max_length=45)
    school_name = models.ForeignKey('School', on_delete=models.CASCADE, db_column='school_name')

    class Meta:
        db_table = 'department'
        unique_together = (('name'),)


class User(models.Model):
    userid = models.AutoField(db_column='userID', primary_key=True)  # Field name made lowercase.
    school_name = models.ForeignKey(School, on_delete=models.CASCADE, db_column='school_name')
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='department_name')
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=45, blank=True, null=True)
    profile_photo = models.CharField(max_length=250)
    gender = models.CharField(max_length=45, choices=[('male', 'male'), ('female', 'female')])
    role = models.CharField(max_length=45, choices=[('student', 'student'),('instructor','instructor'),('admin','admin')])

    class Meta:
        db_table = 'user'
        unique_together = (('userid', 'first_name'),)


class Instructor(models.Model):
    instructorid = models.AutoField(db_column='instructorID', primary_key=True)  # Field name made lowercase.
    user_userid = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_userID')  # Field name made lowercase.
    position = models.CharField(max_length=45)

    class Meta:
        db_table = 'instructor'
        unique_together = (('instructorid', 'user_userid'),)


class Student(models.Model):
    studentid = models.AutoField(db_column='studentID', primary_key=True)  # Field name made lowercase.
    user_userid = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_userID')  # Field name made lowercase.
    level = models.CharField(max_length=45, choices=[('Foundation', 'Foundation'),('Undegraduate','Undegraduate'),('Graduate','Graduate'), ('Phd','Phd')])
    year_of_study = models.IntegerField(choices=[(0, 0),(1,1),(2,2),(3,3), (4,4)])
    academic_status = models.CharField(max_length=45, choices=[('Good', 'Good'),('Probation','Probation')])
    schedule_approve = models.BooleanField(default=False)
    schedule_lock = models.BooleanField(default=False)

    class Meta:
        db_table = 'student'
        unique_together = (('studentid', 'user_userid'),)


class Course(models.Model):
    courseid = models.AutoField(db_column='courseID', primary_key=True)  # Field name made lowercase.
    course_code = models.CharField(max_length=45)
    title = models.CharField(max_length=45)
    credits = models.IntegerField()
    level = models.CharField(max_length=45, choices=[('Foundation', 'Foundation'),('Undegraduate','Undegraduate'),('Graduate','Graduate'), ('Phd','Phd')])
    description = models.CharField(max_length=250)
    department_name = models.ForeignKey('Department', on_delete=models.CASCADE, db_column='department_name')

    class Meta:
        db_table = 'course'
        unique_together = (('courseid', 'title', 'department_name'),)


class Priority(models.Model):
    year = models.IntegerField(choices=[(0,0),(1,1),(2,2),(3,3),(4,4)])
    course_courseid = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='course_courseID')  # Field name made lowercase.
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='department_name')
    type = models.IntegerField(choices=[(1,1),(2,2),(3,3)])

    class Meta:
        db_table = 'priority'
        unique_together = (('course_courseid', 'department_name', 'year'),)
        verbose_name = 'Priority for Course'


class Requisite(models.Model):
    course_courseid = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='course_courseID')  # Field name made lowercase.
    req_course_courseid = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='req_course_courseID', related_name='requisite_course')  # Field name made lowercase.
    type = models.CharField(max_length=45, choices=[('pre-requisite', 'pre-requisite'),('co-requisite','co-requisite'),('anti-requisite','anti-requisite')])
    is_optional = models.BooleanField(default=False)

    class Meta:
        db_table = 'requisite'
        unique_together = (('course_courseid', 'req_course_courseid'),)


class Registrationdate(models.Model):
    registrationid = models.AutoField(db_column='registrationID', primary_key=True)  # Field name made lowercase.
    priority = models.IntegerField(choices=[(1,1),(2,2),(3,3)])
    year = models.IntegerField(choices=[(0,0),(1,1),(2,2),(3,3),(4,4)])
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()

    class Meta:
        db_table = 'registrationDate'
        verbose_name = 'Registration Date'


class Coursesection(models.Model):
    sectionid = models.AutoField(db_column='sectionID', primary_key=True)  # Field name made lowercase.
    course_courseid = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='course_courseID')  # Field name made lowercase.
    num_type = models.CharField(max_length=45)
    section_type = models.CharField(max_length=45, choices=[('Lecture', 'Lecture'),('Seminar','Seminar'),('Recitation','Recitation'), ('Lab', 'Lab')], default='Lecture')
    start_time = models.TimeField()
    end_time = models.TimeField()
    semester = models.CharField(max_length=45, choices=[('Fall', 'Fall'),('Spring','Spring'),('Summer','Summer')])
    year = models.IntegerField()
    capacity = models.IntegerField()
    room = models.CharField(max_length=45)
    total_points = models.IntegerField()

    class Meta:
        db_table = 'courseSection'
        unique_together = (('sectionid', 'course_courseid'),)
        verbose_name = 'Course Section'


class Sectionday(models.Model):
    coursesection_sectionid = models.ForeignKey(Coursesection, on_delete=models.CASCADE, db_column='courseSection_sectionID')  # Field name made lowercase.
    day = models.CharField(max_length=45, choices=[('1', 'Monday'),('2','Tuesday'),('3','Wednesday'), ('4','Thursday'),('5','Friday'),('6','Saturday')])

    class Meta:
        db_table = 'sectionDay'
        verbose_name = 'Section Day'


class Advice(models.Model):
    instructor_instructorid = models.ForeignKey('Instructor', on_delete=models.CASCADE, db_column='instructor_instructorID')  # Field name made lowercase.
    student_studentid = models.ForeignKey('Student', on_delete=models.CASCADE, db_column='student_studentID')  # Field name made lowercase.

    class Meta:
        db_table = 'advice'
        unique_together = (('instructor_instructorid', 'student_studentid'),)
        verbose_name = 'Student Advisor'


class CourseInstructor(models.Model):
    instructor_instructorid = models.ForeignKey('Instructor', on_delete=models.CASCADE, db_column='instructor_instructorID')  # Field name made lowercase.
    coursesection_sectionid = models.ForeignKey(Coursesection, on_delete=models.CASCADE, db_column='courseSection_sectionID')   # Field name made lowercase.

    class Meta:
        db_table = 'course_instructor'
        unique_together = (('instructor_instructorid', 'coursesection_sectionid'),)
        verbose_name = 'Course Instructor'


class StudentEnrollment(models.Model):
    student_studentid = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student_studentID')  # Field name made lowercase.
    coursesection_sectionid = models.ForeignKey(Coursesection, on_delete=models.CASCADE, db_column='courseSection_sectionID')   # Field name made lowercase.

    class Meta:
        db_table = 'student_enrollment'
        unique_together = (('student_studentid', 'coursesection_sectionid'),)
        verbose_name = 'Student Enrollment'


class CourseGrades(models.Model):
    student_studentid = models.ForeignKey('Student', on_delete=models.CASCADE, db_column='student_studentID')  # Field name made lowercase.
    coursesection_sectionid = models.ForeignKey(Coursesection, on_delete=models.CASCADE, db_column='courseSection_sectionID')   # Field name made lowercase.
    midterm_grade = models.CharField(max_length=45, blank=True, null=True, choices=[('S','S'),('NS','NS')])
    final_grade = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'course_grades'
        unique_together = (('student_studentid', 'coursesection_sectionid'),)
        verbose_name = 'Student Grade'


class Coursepagemodule(models.Model):
    moduleid = models.AutoField(db_column='moduleID', primary_key=True)  # Field name made lowercase.
    coursesection_sectionid = models.ForeignKey('Coursesection', on_delete=models.CASCADE, db_column='courseSection_sectionID')  # Field name made lowercase.
    title = models.CharField(max_length=100)
    order = models.IntegerField()

    class Meta:
        db_table = 'coursePageModule'
        unique_together = (('moduleid', 'coursesection_sectionid'),)
        verbose_name = 'Course Page Module'


class Announcement(models.Model):
    announcementid = models.AutoField(db_column='announcementID', primary_key=True)  # Field name made lowercase.
    coursesection_sectionid = models.ForeignKey('Coursesection', on_delete=models.CASCADE, db_column='courseSection_sectionID')  # Field name made lowercase.
    text = models.CharField(max_length=250)
    date = models.DateTimeField()

    class Meta:
        db_table = 'announcement'
        unique_together = (('announcementid', 'coursesection_sectionid'),)


class AnnouncementNotification(models.Model):
    user_userid = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_userID')  # Field name made lowercase.
    notify_object_id = models.IntegerField()
    time = models.TimeField()
    is_turned_on = models.BooleanField(default=False)

    class Meta:
        db_table = 'announcement_notification'


class Discussion(models.Model):
    discussionid = models.AutoField(db_column='discussionID', primary_key=True)  # Field name made lowercase.
    coursepagemodule_moduleid = models.ForeignKey(Coursepagemodule, on_delete=models.CASCADE, db_column='coursePageModule_moduleID')  # Field name made lowercase.
    title = models.CharField(max_length=45)

    class Meta:
        db_table = 'discussion'
        unique_together = (('discussionid', 'coursepagemodule_moduleid'),)


class Post(models.Model):
    user_userid = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_userID')  # Field name made lowercase.
    discussion_discussionid = models.ForeignKey(Discussion, on_delete=models.CASCADE, db_column='discussion_discussionID')  # Field name made lowercase.
    text = models.CharField(max_length=250)
    date = models.DateTimeField()

    class Meta:
        db_table = 'post'
        unique_together = (('user_userid', 'discussion_discussionid'),)


class Assignment(models.Model):
    assignmentid = models.AutoField(db_column='assignmentID', primary_key=True)  # Field name made lowercase.
    coursepagemodule_moduleid = models.ForeignKey('Coursepagemodule',  on_delete=models.CASCADE, db_column='coursePageModule_moduleID')  # Field name made lowercase.
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=250)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    max_point = models.IntegerField()
    class Meta:
        db_table = 'assignment'
        unique_together = (('assignmentid', 'coursepagemodule_moduleid'),)



class Assignmentsubmission(models.Model):
    assignment_assignmentid = models.ForeignKey(Assignment, on_delete=models.CASCADE, db_column='assignment_assignmentID')  # Field name made lowercase.
    student_studentid = models.ForeignKey('Student', on_delete=models.CASCADE, db_column='student_studentID')  # Field name made lowercase.
    # date = models.DateField(unique=True, blank=True, null=True)
    date = models.DateTimeField(null=True)
    points = models.IntegerField()
    feedback = models.CharField(max_length=250, blank=True, null=True)
    myFile = models.FileField(default="default.jpg")

    class Meta:
        db_table = 'assignmentSubmission'
        unique_together = (('assignment_assignmentid', 'student_studentid'),)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)


class Quiz(models.Model):
    quizid = models.AutoField(db_column='quizID', primary_key=True)  # Field name made lowercase.
    coursepagemodule_moduleid = models.ForeignKey(Coursepagemodule, on_delete=models.CASCADE, db_column='coursePageModule_moduleID')  # Field name made lowercase.
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=250)
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
    time_limit = models.IntegerField()
    max_point = models.IntegerField()

    class Meta:
        db_table = 'quiz'
        unique_together = (('quizid', 'coursepagemodule_moduleid'),)


class Quizquestion(models.Model):
    questionid = models.AutoField(db_column='questionID', primary_key=True)  # Field name made lowercase.
    quiz_quizid = models.ForeignKey(Quiz, on_delete=models.CASCADE, db_column='quiz_quizID')  # Field name made lowercase.
    text = models.CharField(max_length=250)
    is_open = models.BooleanField(default=False)
    points = models.IntegerField()
    is_ans = models.BooleanField(default=False)
    friend = models.IntegerField(default=-1)
    textTwo = models.CharField(max_length=250, default='default value')
    class Meta:
        db_table = 'quizQuestion'
        unique_together = (('questionid', 'quiz_quizid'),)


class Answerchoice(models.Model):
    answerid = models.AutoField(db_column='answerID', primary_key=True)  # Field name made lowercase.
    quizquestion_questionid = models.ForeignKey('Quizquestion', on_delete=models.CASCADE, db_column='quizQuestion_questionID')  # Field name made lowercase.
    text = models.CharField(max_length=45)
    is_right = models.BooleanField(default=False)

    class Meta:
        db_table = 'answerChoice'
        unique_together = (('answerid', 'quizquestion_questionid'),)


class Quizsubmission(models.Model):
    student_studentid = models.ForeignKey('Student', on_delete=models.CASCADE, db_column='student_studentID')  # Field name made lowercase.
    quiz_quizid = models.ForeignKey(Quiz, on_delete=models.CASCADE, db_column='quiz_quizID')  # Field name made lowercase.
    answerchoice_answerid = models.OneToOneField(Answerchoice, on_delete=models.CASCADE, db_column='answerChoice_answerID')  # Field name made lowercase.
    quizquestion_questionid = models.OneToOneField(Quizquestion, on_delete=models.CASCADE, db_column='quizQuestion_questionID')  # Field name made lowercase.

    class Meta:
        db_table = 'quizSubmission'
        unique_together = (('student_studentid', 'quizquestion_questionid', 'quiz_quizid', 'answerchoice_answerid'),)


class File(models.Model):
    fileid = models.AutoField(db_column='fileID', primary_key=True)  # Field name made lowercase.
    coursepagemodule_moduleid = models.ForeignKey(Coursepagemodule, on_delete=models.CASCADE, db_column='coursePageModule_moduleID')  # Field name made lowercase.
    # placeName = models.CharField(max_length=45, choices=[('assignment','assignment'), ('submission', 'submission'), ('course', 'course')]) #to identify where from
    # url = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    myFile = models.FileField(default="default.jpg")
    class Meta:
        db_table = 'file'
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)