# Generated by Django 2.2.12 on 2020-11-16 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alldata', '0019_remove_assignment_myfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='myFile',
            field=models.FileField(default='default.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
