from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    academy = models.IntegerField()
    avatar = models.CharField(max_length=200)

    class Meta:
        db_table = 'Student'


class Admin(models.Model):
    staff_id = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=32)
    avatar = models.CharField(max_length=200)
    is_super_admin = models.BooleanField()

    class Meta:
        db_table = 'Admin'


class Notification(models.Model):
    notification_id = models.IntegerField(max_length=32)
    student = models.ForeignKey(to="Student", on_delete=models.CASCADE)
    reason = models.CharField(max_length=64)
    time_slot = models.TimeField()
    read = models.BooleanField()
    admin = models.ForeignKey(to="Admin", on_delete=models.CASCADE)

    class Meta:
        db_table = "Notification"
