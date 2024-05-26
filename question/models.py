from django.db import models
from .lib.static_var import *
from django.core.validators import MinValueValidator, MaxValueValidator

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

