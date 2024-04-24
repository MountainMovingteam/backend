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


class Admin(models.Model):
    staff_id = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=32)
    avatar = models.CharField(max_length=200)
    is_super_admin = models.BooleanField()
