from django.contrib import admin
from .models import Course, Lesson, Student, Homework


admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Student)
admin.site.register(Homework)