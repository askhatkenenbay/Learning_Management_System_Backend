from django.db import models

class School(models.Model):
    name = models.CharField(primary_key=True, max_length=45)

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
    profile_photo = models.CharField(max_length=45)
    gender = models.CharField(max_length=45)
    role = models.CharField(max_length=45)

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
    level = models.CharField(max_length=45)
    year_of_study = models.IntegerField()
    academic_status = models.CharField(max_length=45)
    schedule_approve = models.BooleanField(default=False)
    schedule_lock = models.BooleanField(default=False)

    class Meta:
        db_table = 'student'
        unique_together = (('studentid', 'user_userid'),)