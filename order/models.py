from django.db import models


# Create your models here.
class Place(models.Model):
    week_num = models.IntegerField()
    time_index = models.IntegerField()  # 1-58 从周一开始
    capacity = models.IntegerField()
    status = models.IntegerField()


class Order(models.Model):
    place = models.ForeignKey(to="Place", on_delete=models.CASCADE)
    user_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    academy = models.IntegerField()
    is_person = models.BooleanField()
    team = models.ForeignKey(to="Team", on_delete=models.CASCADE)


class Team(models.Model):
    leader_name = models.CharField(max_length=64)
    leader_id = models.CharField(max_length=64)
    leader_phone = models.CharField(max_length=64)
    academy = models.IntegerField()


class TeamMember(models.Model):
    team = models.ForeignKey(to="Team", on_delete=models.CASCADE)
    member_id = models.CharField(max_length=64)
    member_name = models.CharField(max_length=64)
