from django.contrib import admin
# import your models here
from .models import Course, Lesson

# Register your models here
admin.site.register(Course)
admin.site.register(Lesson)
