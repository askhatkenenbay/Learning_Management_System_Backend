from django.contrib import admin
from .models import *


admin.site.site_header = 'Nazarbayev University'

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_name')
admin.site.register(School, SchoolAdmin)


class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('name', 'school_name')
admin.site.register(Department, DepartmentAdmin)


class UserAdmin(admin.ModelAdmin):
	list_display = ('userid', 'first_name', 'last_name', 'email', 'role')
admin.site.register(User, UserAdmin)


class StudentAdmin(admin.ModelAdmin):
	list_display = ('studentid', 'name', 'level', 'year_of_study', 'academic_status')

	def name(self, obj):
		return (obj.user_userid.first_name, obj.user_userid.last_name)
admin.site.register(Student, StudentAdmin)


class InstructorAdmin(admin.ModelAdmin):
	list_display = ('instructorid', 'name', 'position')

	def name(self, obj):
		return (obj.user_userid.first_name, obj.user_userid.last_name)
admin.site.register(Instructor, InstructorAdmin)


class CourseAdmin(admin.ModelAdmin):
	list_display = ('course_code', 'title', 'department_name')
admin.site.register(Course, CourseAdmin)


class PriorityAdmin(admin.ModelAdmin):
	list_display = ('course_name', 'type', 'year')

	def course_name(self, obj):
		return (obj.course_courseid.title)
admin.site.register(Priority, PriorityAdmin)

admin.site.register(Requisite)
admin.site.register(Registrationdate)
admin.site.register(Coursesection)
admin.site.register(Sectionday)
admin.site.register(Advice)

class CourseInstructorAdmin(admin.ModelAdmin):
	list_display = ('course', 'instructor')

	def course(self, obj):
		return (obj.coursesection_sectionid.course_courseid.course_code, obj.coursesection_sectionid.course_courseid.title)

	def instructor(self, obj):
		return (obj.instructor_instructorid.user_userid.first_name, obj.instructor_instructorid.user_userid.last_name)
admin.site.register(CourseInstructor, CourseInstructorAdmin)


admin.site.register(StudentEnrollment)
admin.site.register(CourseGrades)
admin.site.register(Coursepagemodule)
#admin.site.register(Announcement)
#admin.site.register(AnnouncementNotification)
#admin.site.register(Discussion)
#admin.site.register(Post)
#admin.site.register(Assignment)
#admin.site.register(Assignmentsubmission)
#admin.site.register(Quiz)
#admin.site.register(Quizquestion)
#admin.site.register(Answerchoice)
#admin.site.register(Quizsubmission)
#admin.site.register(File)
# admin.site.unregister(School)