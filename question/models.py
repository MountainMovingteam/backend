from django.db import models
from mysite.lib.static_var import *
from django.core.validators import MinValueValidator, MaxValueValidator
from base.models import Student
# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=MAX_TITLE_LEN)
    A_content = models.CharField(max_length=MAX_CHOICE_LEN)
    B_content = models.CharField(max_length=MAX_CHOICE_LEN)
    C_content = models.CharField(max_length=MAX_CHOICE_LEN)
    D_content = models.CharField(max_length=MAX_CHOICE_LEN)
    answer = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(15)]
    )
    type = models.IntegerField()

    class Meta:
        db_table = 'Question'


class StudentMapQuestion(models.Model):
    user = models.ForeignKey(to="base.Student", on_delete=models.CASCADE)
    question = models.ForeignKey(to="Question", on_delete=models.CASCADE)
    student_ans = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(15)]
    )

    class Meta:
        db_table = 'StudentMapQuestion'