from django.forms import ModelForm
from .models import Lesson, Homework

class LessonForm(ModelForm):
  class Meta:
    model = Lesson
    fields = ['unit', 'title', 'description']

class HomeworkForm(ModelForm):
  class Meta:
    model = Homework
    fields = ['task', 'due_date']    
