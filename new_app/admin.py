from django.contrib import admin

from .models import School, Student, Course, Enrolment

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'strenth')
    search_fields = ('name', 'location')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fees', 'cls', 'school')
    search_fields = ('name', 'fees', 'school')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('crs_id', 'title', 'strength', 'school')
    search_fields = ('title', 'school')

class EnrolmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course')
    search_fields = ('student', 'course')

admin.site.register(School, SchoolAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrolment, EnrolmentAdmin)