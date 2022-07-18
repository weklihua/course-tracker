from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course
from .forms import LessonForm


# Create your views here.


# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def courses_index(request):
  courses = Course.objects.all()
  return render(request, 'courses/index.html', { 'courses': courses })

def courses_detail(request, course_id):
  course = Course.objects.get(id=course_id)
  lesson_form = LessonForm()
  return render(request, 'courses/detail.html', { 'course': course, 'lesson_form': lesson_form })

class CourseCreate(CreateView):
  model = Course
  fields = '__all__'

class CourseUpdate(UpdateView):
  model = Course
  fields = ['subject', 'teacher', 'day', 'time', 'description', 'prereq']

class CourseDelete(DeleteView):
  model = Course
  success_url = '/courses/'