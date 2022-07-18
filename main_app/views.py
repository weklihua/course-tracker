from django.shortcuts import render, redirect
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

def add_lesson(request, course_id):
  form = LessonForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the course_id assigned
    new_lesson = form.save(commit=False)
    new_lesson.course_id = course_id
    new_lesson.save()
  return redirect('detail', course_id=course_id)

class CourseCreate(CreateView):
  model = Course
  fields = '__all__'

class CourseUpdate(UpdateView):
  model = Course
  fields = ['subject', 'teacher', 'day', 'time', 'description', 'prereq']

class CourseDelete(DeleteView):
  model = Course
  success_url = '/courses/'