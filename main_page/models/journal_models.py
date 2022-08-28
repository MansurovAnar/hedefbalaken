from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from main_page.models.all_models import TeacherProfile, StudentProfile

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from django import forms


class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attended_teacher')
    attended = models.BooleanField(blank=True)
    attendance_date = models.DateField(timezone.now)

    def __str__(self):
        return self.teacher

    class Meta:
        app_label = "main_page"

class StAttendance(models.Model):
    student = models.CharField(max_length=100)
    first_hour = models.BooleanField(default=False)
    second_hour = models.BooleanField(default=False)
    attendance_date = models.DateField(default=timezone.now)

    def get_attendance_count(self):
        pass

    def __str__(self):
        return self.student + " ~ " + str(self.attendance_date)

    def get_unattendance_count(self):
        if (self.first_hour == False) and (self.second_hour == False):
            return 2
        elif (self.first_hour == True) and (self.second_hour == True):
            return 0
        else:
            return 1

    class Meta:
        app_label = "main_page"