from django.contrib import admin
from .models import Course, Lesson, Student, Photo


admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Student)
admin.site.register(Photo)