from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.views.generic import ListView, DetailView
from .models import Course, Student
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
  id_list = course.students.all().values_list('id')
  students_not_in_course = Student.objects.exclude(id__in=id_list)
  lesson_form = LessonForm()
  return render(request, 'courses/detail.html', { 'course': course, 'lesson_form': lesson_form, 'students': students_not_in_course})

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

class StudentList(ListView):
  model = Student

class StudentDetail(DetailView):
  model = Student

class StudentCreate(CreateView):
  model = Student
  fields = '__all__'

class StudentUpdate(UpdateView):
  model = Student
  fields = ['name', 'year']

class StudentDelete(DeleteView):
  model = Student
  success_url = '/students/'

def assoc_student(request, course_id, student_id):
  course = Course.objects.get(id=course_id)
  course.students.add(student_id)
  return redirect('detail', course_id=course_id)

def unassoc_student(request, course_id, student_id):
  course = Course.objects.get(id=course_id)
  course.students.remove(student_id)
  return redirect('detail', course_id=course_id)