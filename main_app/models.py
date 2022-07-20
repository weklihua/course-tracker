from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

DAYS = (
    ("M", "M-W-F"),
    ("T", "T-TH"),
)
TIMES = (
    ("1", "8:00-9:30 am"),
    ("2", "9:30-11:00 am"),
    ("3", "12:00-1:30 pm"),
    ("4", "1:30-3:00 pm")
)
YEARS = (
    ("0", "Kindergarten"),
    ("1", "1st Grade"),
    ("2", "2nd Grade"),
    ("3", "3rd Grade"),
    ("4", "4th Grade"),
    ("5", "5th Grade"),
    ("6", "6th Grade"),
    ("7", "7th Grade"),
    ("8", "8th Grade"),
    ("9", "Freshman"),
    ("10", "Sophomore"),
    ("11", "Junior"),
    ("12", "Senior"),
)

LD = (
    ("n", "No"),
    ("y", "Yes"),
)

class Student(models.Model):
  name = models.CharField(max_length=50)
  year = models.CharField(max_length=2, choices=YEARS, default=YEARS[0][0])
  learning_difference = models.CharField(max_length=2, choices=LD, default=LD[0][0])

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('students_detail', kwargs={'pk': self.id})

class Course(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    day = models.CharField(max_length=1, choices=DAYS, default=DAYS[0][0])
    time = models.CharField(max_length=1, choices=TIMES, default=TIMES[0][0])
    description = models.TextField(max_length=250)
    teacher = models.CharField(max_length=100)
    prereq = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'course_id': self.id})

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    unit = models.PositiveIntegerField(default=1)
    description = models.TextField(max_length=250)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        ordering = ['unit']

    def __str__(self):
        return f"Unit {self.unit}: {self.title}"

class Photo(models.Model):
    url = models.CharField(max_length=200)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for student_id: {self.student_id} @{self.url}"