from django.db import models

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

class Course(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    day = models.CharField(max_length=1, choices=DAYS, default=DAYS[0][0])
    time = models.CharField(max_length=1, choices=TIMES, default=TIMES[0][0])
    description = models.TextField(max_length=250)
    teacher = models.CharField(max_length=100)
    prereq = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.id})"
