# Generated by Django 3.1.2 on 2020-11-09 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alldata', '0013_delete_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('fileid', models.AutoField(db_column='fileID', primary_key=True, serialize=False)),
                ('placeid', models.IntegerField(db_column='placeID')),
                ('placeName', models.CharField(choices=[('assignment', 'assignment'), ('submission', 'submission'), ('course', 'course')], max_length=45)),
                ('url', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'file',
            },
        ),
    ]
