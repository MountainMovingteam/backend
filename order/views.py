import json
from .lib import time
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Place, Order, Team, TeamMember
from manager.models import Lecturer, LecturerPlace
from manager.lib.static_var import *
from manager.lib.static_response import *
from manager.lib.static_fun import *


# from ..manager.models import Lecturer, LecturerPlace


# Create your views here.

def person(request):
    response = user_auth(request)

    if response is not None:
        return response

    data = json.loads(request.body.decode('utf-8'))

    week_num, time_index = time.trans_index(data['time_index'])
    if week_num < 0 or week_num > WEEK_NUM:
        return week_num_illegal()

    if time_index < 0 or time_index > TIMR_INDEX_NUM:
        return time_index_illegal()

    place = Place.objects.filter(week_num=week_num, time_index=time_index).first()
    if place is None:
        return place_not_exists()

    if place.capacity > count_order(place.id):
        Order.objects.create(place=place, user_id=data['id'], name=data['name'], phone=data['phone'],
                             academy=data['academy'], is_person=True)
        return success_respond()
    else:
        return place_full()


def group(request):
    response = user_auth(request)

    if response is not None:
        return response

    data = json.loads(request.body.decode('utf-8'))
    week_num, time_index = time.trans_index(data['time_index'])
    if week_num < 0 or week_num > WEEK_NUM:
        return week_num_illegal()

    if time_index < 0 or time_index > TIMR_INDEX_NUM:
        return time_index_illegal()

    place = Place.objects.filter(week_num=week_num, time_index=time_index).first()
    if place is None:
        return place_not_exists()

    if place.capacity <= count_order(place.id):
        return place_full()

    if have_group(place.id):
        return place_has_group()

    team = Team.objects.create(leader_name=data['leader']['name'], leader_id=data['leader']['id'],
                               leader_phone=data['leader']['phone'], academy=data['academy'])
    persons = data['persons']
    for person in persons:
        TeamMember.objects.create(team=team, member_id=person['id'], member_name=person['name'])
    Order.objects.create(place=place, user_id=data['leader']['id'], name=data['leader']['name'],
                         phone=data['leader']['phone'],
                         academy=data['academy'], is_person=False, team=team)
    return success_respond()


def get_info(request):
    response = user_auth(request)

    if response is not None:
        return response

    details = []
    for time_index in range(1, 57, 1):
        week_num, new_time_index = time.trans_index(time_index)
        place = Place.objects.filter(week_num=week_num, time_index=new_time_index).first()
        capacity = 20
        enrolled = count_order(place.id)
        lecturer = ""
        lecturer_with_place = place.lecturerplace_set.all()
        for l in lecturer_with_place:
            lecturer += " " + Lecturer.objects.filter(id=l.lecturer_id).first().name
        if enrolled == 0:
            type = 0
        elif capacity == enrolled:
            type = 2
        else:
            type = 1
        de = {
            "time_index": time_index,
            "capacity": capacity,
            "enrolled": enrolled,
            "lecturer": lecturer,
            "type": type
        }
        details.append(de)
    return JsonResponse(details, safe=False)


def init_place(request):
    for week_num in range(1, WEEK_NUM + 1, 1):
        for time_index in range(1, TIMR_INDEX_NUM + 1, 1):
            if len(Place.objects.filter(week_num=week_num, time_index=time_index)) == 0:
                Place.objects.create(week_num=week_num, time_index=time_index, capacity=PLACE_CAPACITY)
    return JsonResponse({'success': True})


def clear_place(request):
    Place.objects.all().delete()
    return JsonResponse({'success': True})


def count_order(place_id):
    count = Order.objects.filter(place_id=place_id, is_person=True).count()
    order_with_team = Order.objects.filter(place_id=place_id, is_person=False).select_related('team').first()
    if order_with_team:
        team_with_member = TeamMember.objects.select_related('team').filter(team_id=order_with_team.team_id).all()
        count += len(team_with_member)
    return count


def have_group(place_id):
    count = Order.objects.filter(place_id=place_id, is_person=False).count()
    return count == 1
