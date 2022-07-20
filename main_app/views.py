from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Student, Lesson, Homework
from .forms import LessonForm, HomeworkForm
from .models import Course, Student, Photo
from .forms import LessonForm
from datetime import date
import uuid
import boto3
import os


# Create your views here.


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


@login_required
def courses_index(request):
    courses = Course.objects.filter(user=request.user)
    return render(request, "courses/index.html", {"courses": courses})


@login_required
def courses_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    id_list = course.students.all().values_list("id")
    students_not_in_course = Student.objects.exclude(id__in=id_list)
    lesson_form = LessonForm()
    return render(
        request,
        "courses/detail.html",
        {
            "course": course,
            "lesson_form": lesson_form,
            "students": students_not_in_course,
        },
    )


@login_required
def add_lesson(request, course_id):
    form = LessonForm(request.POST)
    if form.is_valid():
        new_lesson = form.save(commit=False)
        new_lesson.course_id = course_id
        new_lesson.save()
    return redirect("detail", course_id=course_id)


class CourseCreate(LoginRequiredMixin, CreateView):
    model = Course
    fields = ["title", "subject", "teacher", "day", "time", "description", "prereq"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CourseUpdate(LoginRequiredMixin, UpdateView):
    model = Course
    fields = ["subject", "teacher", "day", "time", "description", "prereq"]


class CourseDelete(LoginRequiredMixin, DeleteView):
    model = Course
    success_url = "/courses/"


class StudentList(LoginRequiredMixin, ListView):
    model = Student


class StudentDetail(LoginRequiredMixin, DetailView):
    model = Student

class StudentCreate(LoginRequiredMixin, CreateView):
    model = Student
    fields = "__all__"


class StudentUpdate(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ["name", "year", "learning_difference"]


class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = "/students/"


@login_required
def lessons_detail(request, pk):
  lesson = Lesson.objects.get(id=pk)
  homework_form = HomeworkForm()
  return render(request, 'main_app/lesson_detail.html', {'lesson': lesson, 'homework_form': homework_form})
  
@login_required
def add_homework(request, pk):
  form = HomeworkForm(request.POST)
  if form.is_valid():
    new_homework = form.save(commit=False)
    new_homework.lesson_id = pk
    new_homework.assign_date = date.today()
    new_homework.save()
  return redirect('lessons_detail', pk=pk) 

class LessonUpdate(LoginRequiredMixin, UpdateView):
  model = Lesson
  fields = ['title', 'unit', 'description']

class LessonDelete(LoginRequiredMixin, DeleteView):
  model = Lesson
  success_url = '/courses/' 



@login_required
def assoc_student(request, course_id, student_id):
    Course.objects.get(id=course_id).students.add(student_id)
    return redirect("detail", course_id=course_id)


@login_required
def unassoc_student(request, course_id, student_id):
    course = Course.objects.get(id=course_id)
    course.students.remove(student_id)
    return redirect("detail", course_id=course_id)

def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid sign up - try again"
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)


def add_photo(request, student_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, student_id=student_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('students_detail', pk=student_id)