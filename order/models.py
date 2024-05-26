from django.db import models
from mysite.lib.static_var import *


# Create your models here.
class Place(models.Model):
    week_num = models.IntegerField()
    time_index = models.IntegerField()  # 1-58 从周一开始
    capacity = models.IntegerField(default=PLACE_CAPACITY)
    status = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        db_table = 'Place'


class Order(models.Model):
    place = models.ForeignKey(to="Place", on_delete=models.CASCADE)
    user_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    academy = models.IntegerField()
    is_person = models.BooleanField()
    team = models.ForeignKey(to="Team", on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(default=0)          # 0-未被驳回 1-已被驳回

    class Meta:
        db_table = 'Order'


class Team(models.Model):
    leader_name = models.CharField(max_length=64)
    leader_id = models.CharField(max_length=64)
    leader_phone = models.CharField(max_length=64)
    academy = models.IntegerField()

    class Meta:
        db_table = 'Team'


class TeamMember(models.Model):
    team = models.ForeignKey(to="Team", on_delete=models.CASCADE)
    member_id = models.CharField(max_length=64)
    member_name = models.CharField(max_length=64)

    class Meta:
        db_table = 'TeamMember'
