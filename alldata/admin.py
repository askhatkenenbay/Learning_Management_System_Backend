from django.contrib import admin
from .models import *


admin.site.site_header = 'Nazarbayev University'
admin.site.register(School)
admin.site.register(Department)
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Priority)
admin.site.register(Requisite)
admin.site.register(Registrationdate)
admin.site.register(Coursesection)
admin.site.register(Sectionday)
admin.site.register(Advice)
admin.site.register(CourseInstructor)
admin.site.register(StudentEnrollment)
admin.site.register(CourseGrades)
admin.site.register(Coursepagemodule)
admin.site.register(Announcement)
admin.site.register(AnnouncementNotification)
admin.site.register(Discussion)
admin.site.register(Post)
admin.site.register(Assignment)
admin.site.register(Assignmentsubmission)
admin.site.register(Quiz)
admin.site.register(Quizquestion)
admin.site.register(Answerchoice)
admin.site.register(Quizsubmission)
admin.site.register(File)