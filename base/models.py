from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


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


class EmailVerify(models.Model):
    email = models.CharField(max_length=64)
    code = models.CharField(max_length=256)
    type = models.IntegerField(default=0)
    time_slot = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'EmailVerify'


class Admin(models.Model):
    staff_id = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=32, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    academy = models.IntegerField(null=True, blank=True)
    avatar = models.FileField(upload_to='images/', default='media/default_avatar', null=True, blank=True)

    class Meta:
        db_table = 'Admin'


class Notification(models.Model):
    notification_id = models.CharField(max_length=32)
    student = models.ForeignKey(to="Student", on_delete=models.CASCADE)
    reason = models.CharField(max_length=64, null=True)
    type = models.IntegerField(default=0)  # 0-驳回 1-提醒
    time_slot = models.CharField(max_length=256)
    read = models.BooleanField(default=0)  # 0-未读 1-已读
    admin = models.ForeignKey(to="Admin", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "Notification"


class Picture(models.Model):
    image = models.FileField(upload_to='pictures/')

    class Meta:
        db_table = 'Picture'


class Push(models.Model):
    push_id = models.IntegerField()
    title = models.CharField(max_length=64)
    pre_content = models.CharField(max_length=64)
    picture = models.FileField(upload_to='pushes/')
    address = models.CharField(max_length=256, default=None)

    class Meta:
        db_table = 'Push'
