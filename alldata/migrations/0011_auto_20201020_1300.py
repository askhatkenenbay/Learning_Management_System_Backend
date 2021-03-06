# Generated by Django 3.1.2 on 2020-10-20 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alldata', '0010_school_full_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advice',
            options={'verbose_name': 'Student Advisor'},
        ),
        migrations.AlterModelOptions(
            name='coursegrades',
            options={'verbose_name': 'Student Grade'},
        ),
        migrations.AlterModelOptions(
            name='courseinstructor',
            options={'verbose_name': 'Course Instructor'},
        ),
        migrations.AlterModelOptions(
            name='coursepagemodule',
            options={'verbose_name': 'Course Page Module'},
        ),
        migrations.AlterModelOptions(
            name='coursesection',
            options={'verbose_name': 'Course Section'},
        ),
        migrations.AlterModelOptions(
            name='priority',
            options={'verbose_name': 'Priority for Course'},
        ),
        migrations.AlterModelOptions(
            name='registrationdate',
            options={'verbose_name': 'Registration Date'},
        ),
        migrations.AlterModelOptions(
            name='sectionday',
            options={'verbose_name': 'Section Day'},
        ),
        migrations.AlterModelOptions(
            name='studentenrollment',
            options={'verbose_name': 'Student Enrollment'},
        ),
        migrations.RenameField(
            model_name='quiz',
            old_name='max_poit',
            new_name='max_point',
        ),
        migrations.RemoveField(
            model_name='file',
            name='type',
        ),
        migrations.AddField(
            model_name='course',
            name='course_code',
            field=models.CharField(default=1, max_length=45),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coursegrades',
            name='coursesection_sectionid',
            field=models.ForeignKey(db_column='courseSection_sectionID', default=1, on_delete=django.db.models.deletion.CASCADE, to='alldata.coursesection'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='courseinstructor',
            name='coursesection_sectionid',
            field=models.ForeignKey(db_column='courseSection_sectionID', default=1, on_delete=django.db.models.deletion.CASCADE, to='alldata.coursesection'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coursesection',
            name='year',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='placeName',
            field=models.CharField(choices=[('assignment', 'assignment'), ('submission', 'submission'), ('course', 'course')], default=1, max_length=45),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentenrollment',
            name='coursesection_sectionid',
            field=models.ForeignKey(db_column='courseSection_sectionID', default=1, on_delete=django.db.models.deletion.CASCADE, to='alldata.coursesection'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='text',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='description',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='feedback',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.CharField(choices=[('Foundation', 'Foundation'), ('Undegraduate', 'Undegraduate'), ('Graduate', 'Graduate'), ('Phd', 'Phd')], max_length=45),
        ),
        migrations.AlterField(
            model_name='coursegrades',
            name='midterm_grade',
            field=models.CharField(blank=True, choices=[('S', 'S'), ('NS', 'NS')], max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='coursepagemodule',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='coursesection',
            name='semester',
            field=models.CharField(choices=[('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer')], max_length=45),
        ),
        migrations.AlterField(
            model_name='file',
            name='placeid',
            field=models.IntegerField(db_column='placeID'),
        ),
        migrations.AlterField(
            model_name='file',
            name='url',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='priority',
            name='type',
            field=models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3')]),
        ),
        migrations.AlterField(
            model_name='priority',
            name='year',
            field=models.IntegerField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='time_limit',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='text',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='registrationdate',
            name='priority',
            field=models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3')]),
        ),
        migrations.AlterField(
            model_name='registrationdate',
            name='year',
            field=models.IntegerField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]),
        ),
        migrations.AlterField(
            model_name='requisite',
            name='type',
            field=models.CharField(choices=[('pre-requisite', 'pre-requisite'), ('co-requisite', 'co-requisite'), ('anti-requisite', 'anti-requisite')], max_length=45),
        ),
        migrations.AlterField(
            model_name='school',
            name='full_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sectionday',
            name='day',
            field=models.CharField(choices=[('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('R', 'Thursday'), ('F', 'Friday'), ('S', 'Saturday')], max_length=45),
        ),
        migrations.AlterField(
            model_name='student',
            name='academic_status',
            field=models.CharField(choices=[('Good', 'Good'), ('Probation', 'Probation')], max_length=45),
        ),
        migrations.AlterField(
            model_name='student',
            name='level',
            field=models.CharField(choices=[('Foundation', 'Foundation'), ('Undegraduate', 'Undegraduate'), ('Graduate', 'Graduate'), ('Phd', 'Phd')], max_length=45),
        ),
        migrations.AlterField(
            model_name='student',
            name='year_of_study',
            field=models.IntegerField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=45),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('student', 'student'), ('instructor', 'instructor'), ('admin', 'admin')], max_length=45),
        ),
        migrations.AlterUniqueTogether(
            name='coursegrades',
            unique_together={('student_studentid', 'coursesection_sectionid')},
        ),
        migrations.AlterUniqueTogether(
            name='courseinstructor',
            unique_together={('instructor_instructorid', 'coursesection_sectionid')},
        ),
        migrations.AlterUniqueTogether(
            name='studentenrollment',
            unique_together={('student_studentid', 'coursesection_sectionid')},
        ),
        migrations.RemoveField(
            model_name='coursegrades',
            name='course_courseid',
        ),
        migrations.RemoveField(
            model_name='courseinstructor',
            name='course_courseid',
        ),
        migrations.RemoveField(
            model_name='studentenrollment',
            name='course_courseid',
        ),
    ]
