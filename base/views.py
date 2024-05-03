import os.path

from django.http import JsonResponse, HttpResponse, FileResponse
import json
from .models import Student, Admin, Notification, Picture, Push
import jwt
import datetime
from manager.lib.static_response import *
from django.core.files.storage import FileSystemStorage

from mysite import settings


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
            token = jwt.encode({'id': data['id'], 'login_time': login_time, 'role': 1}, 'secret_key', algorithm='HS256',
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
            'message': '密码不一致'
        }, status=404)
    Student.objects.create(student_id=data['id'],
                           name=data['name'],
                           email=data['email'],
                           phone=data['phone'],
                           academy=data['academy'],
                           password=data['password'], )
    token = jwt.encode(
        {'id': data['id'], 'login_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'role': 0},
        'secret_key', algorithm='HS256', headers=headers).decode('ascii')
    rep = JsonResponse({
        'token': token
    })
    return rep


def get_info(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return none_token()
    id, role, is_login = check_token(token)
    if not is_login:
        return login_timeout()
    user = get_user(id, role)
    print(id, role)

    return JsonResponse({
        'student_info': {
            'id': id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'academy': user.academy,
        }
    })


def get_avatar(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return none_token()
    id, role, is_login = check_token(token)
    if not is_login:
        return login_timeout()

    user = get_user(id, role)
    if user.avatar:
        return JsonResponse({
            'avatar_url': user.avatar.url
        })
    return JsonResponse({
        'avatar_url': '/media/default_avatar'
    })


def modify_password(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return none_token()
    id, role, is_login = check_token(token)
    if not is_login:
        return login_timeout()
    user = get_user(id, role)

    data = json.loads(request.body.decode('utf-8'))
    if data['password'] == data['confirmPassword']:
        user.password = data['password']
        user.save()
        return success_respond()
    return JsonResponse({'success': False})


def notice(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return none_token()
    id, role, is_login = check_token(token)
    if not is_login:
        return login_timeout()
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
        return none_token()
    id, role, is_login = check_token(token)
    if not is_login:
        return login_timeout()
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
        return none_token()
    id, role, is_login = check_token(token)
    if not is_login:
        return login_timeout()
    user = get_user(id, role)

    fs = FileSystemStorage()

    new_id = request.POST['id']
    if Student.objects.filter(student_id=new_id) or Admin.objects.filter(staff_id=new_id):
        return user_has_exists()

    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    academy = request.POST['academy']

    if request.FILES.get('avatar', None):
        avatar = request.FILES['avatar']
        filename = fs.save(id, avatar)
        user.avatar = filename
    if role == 0:
        if id:
            user.student_id = id
        if name:
            user.name = name
        if email:
            user.email = email
        if phone:
            user.phone = phone
        if academy:
            user.academy = academy
    elif role == 1:
        if id:
            user.staff_id = id
        if name:
            user.name = name
        if email:
            user.email = email
        if phone:
            user.phone = phone
    user.save()
    return success_respond()


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
