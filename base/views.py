from django.http import JsonResponse, HttpResponse
import json
from .models import Student, Admin, Notification, Picture, Push
import jwt
import datetime
from manager.lib.static_response import *


# Create your views here.

def login(request):
    data = json.loads(request.body.decode('utf-8'))
    user_id = data['id']
    password = data['password']
    user = Student.objects.filter(student_id=user_id, password=password).first()
    login_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if user:
        token = jwt.encode({'id': data['id'], 'login_time': login_time, 'role': 0}, 'secret_key', algorithm='HS256',
                           headers=headers).decode('ascii')
        rep = JsonResponse({
            'token': token,
            'role': 0
        })
        return rep
    else:
        user = Admin.objects.filter(staff_id=user_id, password=password).first()
        if user:
            token = jwt.encode({'id': data['id'], 'login_time': login_time, 'role': 0}, 'secret_key', algorithm='HS256',
                               headers=headers).decode('ascii')
            rep = JsonResponse({
                'token': token,
                'role': 1
            })
            return rep
        else:
            return user_not_exists()


def register(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    if Student.objects.filter(student_id=data['id']):
        return user_has_exists()
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
    token = jwt.encode(
        {'id': data['id'], 'login_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'role': 0},
        'secret_key', algorithm='HS256')
    rep = JsonResponse({
        'token': token
    })
    return rep


def get_info(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return JsonResponse({'success': False})
    id, role, is_login = check_token(token)
    if not is_login:
        return JsonResponse({'success': False})

    user = get_user(id, role)
    return JsonResponse({
        'student_info': {
            'id': id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'academy': user.academy,
            'avatar': user.avatar
        }
    })


def modify_password(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return JsonResponse({'success': False})
    id, role, is_login = check_token(token)
    if not is_login:
        return JsonResponse({'success': False})
    user = get_user(id, role)

    data = json.loads(request.body.decode('utf-8'))
    if data['password'] == data['confirmPassword']:
        user.password = data['password']
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def notice(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return JsonResponse({'success': False})
    id, role, is_login = check_token(token)
    if not is_login:
        return JsonResponse({'success': False})
    user = get_user(id, role)

    nos = Notification.objects.filter(student=user).all()
    notice_list = []
    for no in nos:
        notice_list.append({
            'notice_id': no.notification_id,
            'time': no.time_slot,
            'key_words': no.reason
        })
    return JsonResponse({
        'num': len(nos),
        'notice_list': notice_list
    })


def notice_info(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return JsonResponse({'success': False})
    id, role, is_login = check_token(token)
    if not is_login:
        return JsonResponse({'success': False})
    user = get_user(id, role)

    data = json.loads(request.body.decode('utf-8'))
    no = Notification.objects.filter(student=user, notification_id=data['notice_id']).first()
    return JsonResponse({
        'time': no.time_slot,
        'content': "抱歉，因为" + no.reason + ",您的参观请求已被驳回",
        'key_word': no.reason
    })


def pictures(request):
    pictures = Picture.objects.all()
    list = []
    for pic in pictures:
        list.append(pic.image)
    return JsonResponse({
        'num': len(pictures),
        'pictures': pictures
    })


def push(request):
    data = json.loads(request.body.decode('utf-8'))
    pushes = Push.objects.filter(push_id__range=(data['start'], data['end']))
    list = []
    for push in pushes:
        list.append({
            'id': push.push_id,
            'title': push.title,
            'pre_content': push.pre_content,
            'picture': push.picture
        })
    return JsonResponse({
        'list': list
    })


def edit_info(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return JsonResponse({'success': False})
    id, role, is_login = check_token(token)
    if not is_login:
        return JsonResponse({'success': False})
    user = get_user(id, role)

    data = json.loads(request.body.decode('utf-8'))
    if role == 0:
        if data['id']:
            user.student_id = data['id']
        if data['name']:
            user.name = data['name']
        if data['email']:
            user.email = data['email']
        if data['phone']:
            user.phone = data['phone']
        if data['academy']:
            user.academy = data['academy']
        if data['avatar']:
            user.avatar = data['avatar']
    elif role == 1:
        if data['id']:
            user.staff_id = data['id']
        if data['name']:
            user.name = data['name']
        if data['email']:
            user.email = data['email']
        if data['phone']:
            user.phone = data['phone']
        if data['avatar']:
            user.avatar = data['avatar']
    user.save()
    return JsonResponse({'success': True})


headers = {
    'alg': "HS256",
}


def check_token(token):
    decoded_token = jwt.decode(token, 'secret_key', algorithms='HS256')

    id = decoded_token.get('id')
    login_time = decoded_token.get('login_time')
    role = decoded_token.get('role')
    time_delta = datetime.datetime.now() - datetime.datetime.strptime(login_time, '%Y-%m-%d %H:%M:%S')
    if time_delta > datetime.timedelta(days=1):
        return id, role, False
    return id, role, True


def get_user(id, role):
    if role == 0:
        user = Student.objects.filter(student_id=id).first()
    else:
        user = Admin.objects.filter(staff_id=id).first()
    return user
