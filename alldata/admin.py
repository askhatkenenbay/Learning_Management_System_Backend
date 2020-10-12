from django.contrib import admin

from .models import School, Department, User, Student, Instructor


admin.site.register(School)
admin.site.register(Department)
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Instructor)
