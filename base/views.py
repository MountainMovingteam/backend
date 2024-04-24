from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import json
from django.contrib import auth
from .models import Student, Admin
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def login(request):
    data = json.loads(request.body.decode('utf-8'))
    user_id = data['id']
    password = data['password']
    user = Student.objects.filter(student_id=user_id, password=password).first()
    if user:
        request.session['id'] = user_id
        rep = JsonResponse({
            'token': request.COOKIES.get('sessionid'),
            'role': 0
        })
        return rep
    else:
        user = Admin.objects.filter(staff_id=user_id, password=password).first()
        if user:
            request.session['id'] = user_id
            rep = JsonResponse({
                'token': request.COOKIES.get('sessionid'),
                'role': 1
            })
            return rep
        else:
            return JsonResponse({
                'code': 404,
                'message': '用户不存在'
            })


def register(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    if Student.objects.filter(student_id=data['id']):
        return JsonResponse({
            'code': 200,
            'message': '用户已存在'
        })
    if data['password'] != data['comfirmPassword']:
        return JsonResponse({
            'code': 400,
            'message': '密码不一致'
        })
    Student.objects.create(student_id=data['id'],
                           name=data['name'],
                           email=data['email'],
                           phone=data['phone'],
                           academy=data['academy'],
                           avatar=data['avatar'],
                           password=data['password'], )
    request.session['id'] = data['id']
    rep = JsonResponse({
        'token': request.COOKIES.get('sessionid')
    })
    return rep
