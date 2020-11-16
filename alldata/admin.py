from django.contrib import admin
from .models import *


admin.site.site_header = 'Nazarbayev University'
class StudentInline(admin.TabularInline):
    model = Student

class InstructorInline(admin.TabularInline):
    model = Instructor

class CoursesectionInline(admin.TabularInline):
	model = Coursesection

class SectiondayInline(admin.TabularInline):
	model = Sectionday

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_name')
admin.site.register(School, SchoolAdmin)

class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('name', 'school_name')
admin.site.register(Department, DepartmentAdmin)

class UserAdmin(admin.ModelAdmin):
	list_display = ('userid', 'first_name', 'last_name', 'email', 'role')
	inlines = [StudentInline]
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
	inlines = [CoursesectionInline]
admin.site.register(Course, CourseAdmin)

class PriorityAdmin(admin.ModelAdmin):
	list_display = ('course_name', 'type', 'year')
	def course_name(self, obj):
		return (obj.course_courseid.title)
admin.site.register(Priority, PriorityAdmin)

class RequisiteAdmin(admin.ModelAdmin):
	list_display = ('type', 'course', 'requisite_course', 'is_optional')
	def course(self, obj):
		return (obj.course_courseid.course_code, obj.course_courseid.title)
	def requisite_course(self, obj):
		return (obj.req_course_courseid.course_code, obj.req_course_courseid.title)
admin.site.register(Requisite, RequisiteAdmin)

class RegistrationdateAdmin(admin.ModelAdmin):
	list_display = ('registrationid', 'priority', 'year', 'open_time', 'close_time')
admin.site.register(Registrationdate, RegistrationdateAdmin)

class CoursesectionAdmin(admin.ModelAdmin):
	list_display = ('sectionid', 'course', 'num_type', 'start_time', 'end_time', 'semester', 'year', 'capacity', 'room')
	def course(self, obj):
		return (obj.course_courseid.course_code, obj.course_courseid.title)
	inlines = [SectiondayInline]
admin.site.register(Coursesection, CoursesectionAdmin)

class SectiondayAdmin(admin.ModelAdmin):
	list_display = ('coursesection_sectionid', 'course', 'day')
	def course(self, obj):
		return (obj.coursesection_sectionid.course_courseid.course_code, obj.coursesection_sectionid.course_courseid.title)
admin.site.register(Sectionday, SectiondayAdmin)

class AdviceAdmin(admin.ModelAdmin):
	list_display = ('instructor', 'student')
	def instructor(self, obj):
		return (obj.instructor_instructorid.user_userid.first_name, obj.instructor_instructorid.user_userid.last_name)
	def student(self, obj):
		return (obj.student_studentid.user_userid.first_name, obj.student_studentid.user_userid.last_name)
admin.site.register(Advice, AdviceAdmin)

class CourseInstructorAdmin(admin.ModelAdmin):
	list_display = ('course', 'instructor')
	def course(self, obj):
		return (obj.coursesection_sectionid.course_courseid.course_code, obj.coursesection_sectionid.course_courseid.title)
	def instructor(self, obj):
		return (obj.instructor_instructorid.user_userid.first_name, obj.instructor_instructorid.user_userid.last_name)
admin.site.register(CourseInstructor, CourseInstructorAdmin)

class StudentEnrollmentAdmin(admin.ModelAdmin):
	list_display = ('course', 'student')
	def course(self, obj):
		return (obj.coursesection_sectionid.course_courseid.course_code, obj.coursesection_sectionid.course_courseid.title)
	def student(self, obj):
		return (obj.student_studentid.user_userid.first_name, obj.student_studentid.user_userid.last_name)
admin.site.register(StudentEnrollment, StudentEnrollmentAdmin)

class CourseGradesAdmin(admin.ModelAdmin):
	list_display = ('course', 'student', 'midterm_grade', 'final_grade')
	def course(self, obj):
		return (obj.coursesection_sectionid.course_courseid.course_code, obj.coursesection_sectionid.course_courseid.title)
	def student(self, obj):
		return (obj.student_studentid.user_userid.first_name, obj.student_studentid.user_userid.last_name)
admin.site.register(CourseGrades, CourseGradesAdmin)

class CoursepagemoduleAdmin(admin.ModelAdmin):
	list_display = ('moduleid', 'course', 'title', 'order')
	def course(self, obj):
		return (obj.coursesection_sectionid.course_courseid.course_code, obj.coursesection_sectionid.course_courseid.title)
admin.site.register(Coursepagemodule, CoursepagemoduleAdmin)

admin.site.register(Assignment)

admin.site.register(File)

admin.site.register(Announcement)
admin.site.register(AnnouncementNotification)
admin.site.register(Discussion)
admin.site.register(Post)
admin.site.register(Assignmentsubmission)
admin.site.register(Quiz)
admin.site.register(Quizquestion)
admin.site.register(Answerchoice)
admin.site.register(Quizsubmission)
# admin.site.unregister(School)