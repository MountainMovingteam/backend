import json
from .lib import time
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Place, Order, Team, TeamMember


# Create your views here.

def person(request):
    data = json.loads(request.body.decode('utf-8'))
    week_num, time_index = time.trans_index(data['time_index'])
    place = Place.objects.filter(week_num=week_num, time_index=time_index).first()
    if place['capacity'] > count_order(place['id']):
        Order.objects.create(place=place, user_id=data['id'], name=data['name'], phone=data['phone'],
                             academy=data['academy'], is_person=True)
        return JsonResponse({
            'success': True
        })
    else:
        return JsonResponse({
            'success': False
        })


def group(request):
    data = json.loads(request.body.decode('utf-8'))
    week_num, time_index = time.trans_index(data['time_index'])
    place = Place.objects.filter(week_num=week_num, time_index=time_index).first()
    if place['capacity'] > count_order(place['id']):
        team = Team.objects.create(leader_name=data['leader']['name'], leader_id=data['leader']['id'],
                                   leader_phone=data['leader']['phone'], academy=data['academy'])
        persons = data['persons']
        for person in persons:
            TeamMember.objects.create(team=team, member_id=person['id'], member_name=person['name'])
        Order.objects.create(place=place, user_id=data['id'], name=data['name'], phone=data['phone'],
                             academy=data['academy'], is_person=False, team=team)
        return JsonResponse({
            'success': True
        })
    else:
        return JsonResponse({
            'success': False
        })


def get_info(request):
    pass
    '''week_num = time.get_week_num()
    week_day = time.get_week_day()
    base_index = week_day * 4
    details = []
    for time_index in (1, 28):
        place = Place.objects.filter(week_num=week_num,)
        de = {
            "time_index":time_index,
            "capacity":
        }
    '''

def count_order(place_id):
    count = Order.objects.filter(place_id=place_id, is_person=True).count()
    order_with_team = Order.objects.filter(place_id=place_id, is_person=False).select_related('team').first()
    team_with_member = TeamMember.objects.select_related('team').filter(team_id=order_with_team['team_id']).all()
    count += len(team_with_member)
    return count
