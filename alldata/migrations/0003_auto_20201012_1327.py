# Generated by Django 3.1.2 on 2020-10-12 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alldata', '0002_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='department_name',
            field=models.ForeignKey(db_column='department_name', on_delete=django.db.models.deletion.CASCADE, to='alldata.department'),
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=45)),
                ('year', models.IntegerField()),
                ('course_courseid', models.ForeignKey(db_column='course_courseID', on_delete=django.db.models.deletion.CASCADE, to='alldata.course')),
            ],
            options={
                'db_table': 'priority',
                'unique_together': {('course_courseid', 'type')},
            },
        ),
    ]
