from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Student
from .forms import LessonForm


# Create your views here.


# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def courses_index(request):
  courses = Course.objects.filter(user=request.user)
  return render(request, 'courses/index.html', { 'courses': courses })

@login_required
def courses_detail(request, course_id):
  course = Course.objects.get(id=course_id)
  id_list = course.students.all().values_list('id')
  students_not_in_course = Student.objects.exclude(id__in=id_list)
  lesson_form = LessonForm()
  return render(request, 'courses/detail.html', { 'course': course, 'lesson_form': lesson_form, 'students': students_not_in_course})

@login_required
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


class CourseCreate(LoginRequiredMixin, CreateView):
  model = Course
  fields = ['title', 'subject', 'teacher', 'day', 'time', 'description', 'prereq']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class CourseUpdate(LoginRequiredMixin, UpdateView):
  model = Course
  fields = ['subject', 'teacher', 'day', 'time', 'description', 'prereq']


class CourseDelete(LoginRequiredMixin, DeleteView):
  model = Course
  success_url = '/courses/'



class StudentList(LoginRequiredMixin, ListView):
  model = Student


class StudentDetail(LoginRequiredMixin, DetailView):
  model = Student

class StudentCreate(LoginRequiredMixin, CreateView):
  model = Student
  fields = '__all__'

class StudentUpdate(LoginRequiredMixin, UpdateView):
  model = Student
  fields = ['name', 'year']

class StudentDelete(LoginRequiredMixin, DeleteView):
  model = Student
  success_url = '/students/'

@login_required
def assoc_student(request, course_id, student_id):
  Course.objects.get(id=course_id).students.add(student_id)
  return redirect('detail', course_id=course_id)

@login_required
def unassoc_student(request, course_id, student_id):
  course = Course.objects.get(id=course_id)
  course.students.remove(student_id)
  return redirect('detail', course_id=course_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
 