from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=32, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    academy = models.IntegerField(null=True, blank=True)
    avatar = models.FileField(upload_to='images/', null=True, blank=True)

    class Meta:
        db_table = 'Student'


class Admin(models.Model):
    staff_id = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=32, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    academy = models.IntegerField(null=True, blank=True)
    avatar = models.FileField(upload_to='images/', null=True, blank=True)

    class Meta:
        db_table = 'Admin'


class Notification(models.Model):
    notification_id = models.CharField(max_length=32)
    student = models.ForeignKey(to="Student", on_delete=models.CASCADE)
    reason = models.CharField(max_length=64)
    time_slot = models.TimeField()
    read = models.BooleanField()
    admin = models.ForeignKey(to="Admin", on_delete=models.CASCADE)

    class Meta:
        db_table = "Notification"


class Picture(models.Model):
    image = models.CharField(max_length=200)

    class Meta:
        db_table = 'Picture'


class Push(models.Model):
    push_id = models.IntegerField()
    title = models.CharField(max_length=64)
    pre_content = models.CharField(max_length=64)
    picture = models.CharField(max_length=200)

    class Meta:
        db_table = 'Push'
