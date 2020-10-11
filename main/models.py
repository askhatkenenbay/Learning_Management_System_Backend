# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Advice(models.Model):
    instructor_instructorid = models.OneToOneField('Instructor', models.DO_NOTHING, db_column='instructor_instructorID', primary_key=True)  # Field name made lowercase.
    student_studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='student_studentID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'advice'
        unique_together = (('instructor_instructorid', 'student_studentid'),)


class Announcement(models.Model):
    announcementid = models.AutoField(db_column='announcementID', primary_key=True)  # Field name made lowercase.
    text = models.CharField(max_length=45)
    date = models.DateTimeField()
    coursesection_sectionid = models.ForeignKey('Coursesection', models.DO_NOTHING, db_column='courseSection_sectionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'announcement'
        unique_together = (('announcementid', 'coursesection_sectionid'),)


class AnnouncementNotification(models.Model):
    user_userid = models.OneToOneField('User', models.DO_NOTHING, db_column='user_userID', primary_key=True)  # Field name made lowercase.
    time = models.TimeField()
    is_turned_on = models.IntegerField()
    notify_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'announcement_notification'


class Answerchoice(models.Model):
    answerid = models.AutoField(db_column='answerID', primary_key=True)  # Field name made lowercase.
    text = models.CharField(max_length=45)
    is_right = models.IntegerField()
    quizquestion_questionid = models.ForeignKey('Quizquestion', models.DO_NOTHING, db_column='quizQuestion_questionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'answerChoice'
        unique_together = (('answerid', 'quizquestion_questionid'),)


class Assignment(models.Model):
    assignmentid = models.AutoField(db_column='assignmentID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    max_point = models.IntegerField()
    coursepagemodule_moduleid = models.ForeignKey('Coursepagemodule', models.DO_NOTHING, db_column='coursePageModule_moduleID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'assignment'
        unique_together = (('assignmentid', 'coursepagemodule_moduleid'),)


class Assignmentsubmission(models.Model):
    date = models.DateField(unique=True, blank=True, null=True)
    points = models.CharField(unique=True, max_length=45, blank=True, null=True)
    feedback = models.CharField(max_length=45, blank=True, null=True)
    assignment_assignmentid = models.OneToOneField(Assignment, models.DO_NOTHING, db_column='assignment_assignmentID', primary_key=True)  # Field name made lowercase.
    student_studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='student_studentID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'assignmentSubmission'
        unique_together = (('assignment_assignmentid', 'student_studentid'),)


class Course(models.Model):
    courseid = models.AutoField(db_column='courseID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=45)
    credits = models.IntegerField()
    level = models.IntegerField()
    description = models.CharField(max_length=45)
    department_school_name = models.ForeignKey('Department', models.DO_NOTHING, db_column='department_school_name')

    class Meta:
        managed = False
        db_table = 'course'
        unique_together = (('courseid', 'department_school_name'),)


class Coursepagemodule(models.Model):
    moduleid = models.AutoField(db_column='moduleID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=45)
    order = models.IntegerField()
    coursesection_sectionid = models.ForeignKey('Coursesection', models.DO_NOTHING, db_column='courseSection_sectionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'coursePageModule'
        unique_together = (('moduleid', 'coursesection_sectionid'),)


class Coursesection(models.Model):
    sectionid = models.AutoField(db_column='sectionID', primary_key=True)  # Field name made lowercase.
    num_type = models.CharField(max_length=45)
    start_time = models.CharField(max_length=45)
    end_time = models.CharField(max_length=45)
    semester = models.CharField(max_length=45)
    capacity = models.IntegerField()
    room = models.CharField(max_length=45)
    total_points = models.IntegerField()
    course_courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='course_courseID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'courseSection'
        unique_together = (('sectionid', 'course_courseid'),)


class CourseGrades(models.Model):
    student_studentid = models.OneToOneField('Student', models.DO_NOTHING, db_column='student_studentID', primary_key=True)  # Field name made lowercase.
    course_courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='course_courseID')  # Field name made lowercase.
    midterm_grade = models.CharField(max_length=45, blank=True, null=True)
    final_grade = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_grades'
        unique_together = (('student_studentid', 'course_courseid'),)


class CourseInstructor(models.Model):
    instructor_instructorid = models.OneToOneField('Instructor', models.DO_NOTHING, db_column='instructor_instructorID', primary_key=True)  # Field name made lowercase.
    course_courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='course_courseID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'course_instructor'
        unique_together = (('instructor_instructorid', 'course_courseid'),)


class Department(models.Model):
    name = models.CharField(primary_key=True, max_length=45)
    school_name = models.ForeignKey('School', models.DO_NOTHING, db_column='school_name')

    class Meta:
        managed = False
        db_table = 'department'
        unique_together = (('name', 'school_name'),)


class Discussion(models.Model):
    discussionid = models.AutoField(db_column='discussionID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=45)
    coursepagemodule_moduleid = models.ForeignKey(Coursepagemodule, models.DO_NOTHING, db_column='coursePageModule_moduleID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'discussion'
        unique_together = (('discussionid', 'coursepagemodule_moduleid'),)


class File(models.Model):
    fileid = models.AutoField(db_column='fileID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=45)
    placeid = models.CharField(db_column='placeID', max_length=45)  # Field name made lowercase.
    url = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'file'


class Instructor(models.Model):
    position = models.CharField(max_length=45)
    instructorid = models.AutoField(db_column='instructorID', primary_key=True)  # Field name made lowercase.
    user_userid = models.ForeignKey('User', models.DO_NOTHING, db_column='user_userID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'instructor'
        unique_together = (('instructorid', 'user_userid'),)


class Post(models.Model):
    user_userid = models.OneToOneField('User', models.DO_NOTHING, db_column='user_userID', primary_key=True)  # Field name made lowercase.
    discussion_discussionid = models.ForeignKey(Discussion, models.DO_NOTHING, db_column='discussion_discussionID')  # Field name made lowercase.
    text = models.CharField(max_length=45)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'post'
        unique_together = (('user_userid', 'discussion_discussionid'),)


class Priority(models.Model):
    type = models.CharField(max_length=45)
    year = models.IntegerField()
    course_courseid = models.OneToOneField(Course, models.DO_NOTHING, db_column='course_courseID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'priority'
        unique_together = (('course_courseid'),)


class Quiz(models.Model):
    quizid = models.AutoField(db_column='quizID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    open_time = models.TimeField()
    close_time = models.TimeField()
    time_limit = models.TimeField()
    max_poit = models.IntegerField()
    coursepagemodule_moduleid = models.ForeignKey(Coursepagemodule, models.DO_NOTHING, db_column='coursePageModule_moduleID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quiz'
        unique_together = (('quizid', 'coursepagemodule_moduleid'),)


class Quizquestion(models.Model):
    questionid = models.AutoField(db_column='questionID', primary_key=True)  # Field name made lowercase.
    text = models.CharField(max_length=45)
    is_open = models.IntegerField()
    points = models.IntegerField()
    quiz_quizid = models.ForeignKey(Quiz, models.DO_NOTHING, db_column='quiz_quizID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quizQuestion'
        unique_together = (('questionid', 'quiz_quizid'),)


class Quizsubmission(models.Model):
    student_studentid = models.OneToOneField('Student', models.DO_NOTHING, db_column='student_studentID', primary_key=True)  # Field name made lowercase.
    quizquestion_questionid = models.ForeignKey(Quizquestion, models.DO_NOTHING, db_column='quizQuestion_questionID')  # Field name made lowercase.
    quiz_quizid = models.ForeignKey(Quiz, models.DO_NOTHING, db_column='quiz_quizID')  # Field name made lowercase.
    answerchoice_answerid = models.ForeignKey(Answerchoice, models.DO_NOTHING, db_column='answerChoice_answerID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quizSubmission'
        unique_together = (('student_studentid', 'quizquestion_questionid', 'quiz_quizid', 'answerchoice_answerid'),)


class Registrationdate(models.Model):
    registrationid = models.AutoField(db_column='registrationID', primary_key=True)  # Field name made lowercase.
    priority = models.IntegerField()
    year = models.IntegerField()
    open_time = models.CharField(max_length=45)
    close_time = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'registrationDate'


class Requisite(models.Model):
    course_courseid = models.OneToOneField(Course, models.DO_NOTHING, db_column='course_courseID', primary_key=True)  # Field name made lowercase.
    req_course_courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='req_course_courseID', related_name='requisite_course')  # Field name made lowercase.
    type = models.CharField(max_length=45)
    is_optional = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'requisite'
        unique_together = (('course_courseid', 'req_course_courseid'),)


class School(models.Model):
    name = models.CharField(primary_key=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'school'


class Sectionday(models.Model):
    coursesection_sectionid = models.OneToOneField(Coursesection, models.DO_NOTHING, db_column='courseSection_sectionID', primary_key=True)  # Field name made lowercase.
    day = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sectionDay'


class Student(models.Model):
    level = models.CharField(max_length=45)
    year_of_study = models.IntegerField()
    academic_status = models.CharField(max_length=45)
    schedule_approve = models.IntegerField()
    schedule_lock = models.IntegerField()
    studentid = models.AutoField(db_column='studentID', primary_key=True)  # Field name made lowercase.
    user_userid = models.ForeignKey('User', models.DO_NOTHING, db_column='user_userID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'student'
        unique_together = (('studentid', 'user_userid'),)


class StudentEnrollment(models.Model):
    student_studentid = models.OneToOneField(Student, models.DO_NOTHING, db_column='student_studentID', primary_key=True)  # Field name made lowercase.
    course_courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='course_courseID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'student_enrollment'
        unique_together = (('student_studentid', 'course_courseid'),)


class User(models.Model):
    userid = models.AutoField(db_column='userID', primary_key=True)  # Field name made lowercase.
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=45, blank=True, null=True)
    profile_photo = models.CharField(max_length=45)
    gender = models.CharField(max_length=45)
    role = models.CharField(max_length=45)
    school_name = models.ForeignKey(School, models.DO_NOTHING, db_column='school_name')
    department_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='department_name')

    class Meta:
        managed = False
        db_table = 'user'
        unique_together = (('userid', 'school_name', 'department_name'),)
