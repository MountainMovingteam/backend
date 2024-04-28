from django.db import models


# Create your models here.
class Lecturer(models.Model):
    lecturer_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    tag = models.IntegerField()

    class Meta:
        db_table = 'Lecturer'


class LecturerPlace(models.Model):
    lecturer = models.ForeignKey(to="Lecturer", on_delete=models.CASCADE)
    place = models.ForeignKey(to="order.Place", on_delete=models.CASCADE)

    class Meta:
        db_table = "LecturePlace"
