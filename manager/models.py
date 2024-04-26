from django.db import models


# Create your models here.
class Lecturer(models.Model):
    lecturer_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    tag = models.IntegerField()

