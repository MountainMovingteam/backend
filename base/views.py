import os.path
import random
import string

from django.http import JsonResponse, HttpResponse, FileResponse
import json
from .models import Student, Admin, Notification, Picture, Push
import datetime
import jwt
from manager.lib.static_fun import get_order_log_json
from manager.lib.static_response import *
from django.core.files.storage import FileSystemStorage
from order.models import Order
from manager.lib.static_fun import admin_auth

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
    if Student.objects.filter(student_id=data['id']) or Admin.objects.filter(staff_id=data['id']):
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
    if user is None:
        return user_not_exists()

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
    if user is None:
        return user_not_exists()

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

    if user is None:
        return user_not_exists()

    data = json.loads(request.body.decode('utf-8'))
    if data['password'] == data['confirmPassword']:
        user.password = data['password']
        user.save()
        return success_respond()
    return password_not_match()


def notice(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return none_token()
    id, role, is_login = check_token(token)
    if not is_login:
        return login_timeout()
    user = get_user(id, role)

    if user is None:
        return user_not_exists()

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

    if user is None:
        return user_not_exists()

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
        list.append(pic.image.url)
    return JsonResponse({
        'num': len(pictures),
        'pictures': list
    })


def push(request):
    data = json.loads(request.body.decode('utf-8'))
    total = Push.objects.count()
    pushes = Push.objects.filter(push_id__range=(data['start'], data['end']))
    list = []
    for push in pushes:
        print(push.address)
        list.append({
            'id': push.push_id,
            'title': push.title,
            'pre_content': push.pre_content,
            'picture': push.picture.url,
            'address': push.address
        })
    return JsonResponse({
        'total': total,
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
    if user is None:
        return user_not_exists()

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


def add_picture(request):
    response = admin_auth(request)
    if response is not None:
        return response

    fs = FileSystemStorage()
    picture = Picture()
    if request.FILES.get('image', None):
        image = request.FILES['image']
        filename = fs.save('picture' + generate_random_string(), image)
        picture.image = filename
        picture.save()
        return success_respond()
    return JsonResponse({'success': False, 'reason': 'no picture'}, status=404)


def add_push(request):
    response = admin_auth(request)
    if response is not None:
        return response

    fs = FileSystemStorage()
    push_id = request.POST['push_id']
    if Push.objects.filter(push_id=push_id).count() > 0:
        return JsonResponse({'success': False}, status=404)

    pre_content = request.POST['pre_content']
    title = request.POST['title']
    address = request.POST['address']
    push = Push(push_id=push_id, title=title, pre_content=pre_content, address=address)
    if request.FILES.get('picture', None):
        picture = request.FILES['picture']
        filename = fs.save('push' + push_id, picture)
        push.picture = filename
    push.save()
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


def generate_random_string(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters_and_digits) for i in range(length))
    return random_string


def get_order_log(request):
    print("1")
    token = request.META.get('HTTP_AUTHORIZATION')
    print("1")
    if not token:
        return none_token()
    print("1")
    id, role, is_login = check_token(token)
    print("1")
    if not is_login:
        return login_timeout()

    ans = []
    print("1")
    orders = Order.objects.filter(user_id=id)
    print(orders)
    print("4")
    for order in list(orders):
        print("2")
        ans.append(get_order_log_json(order))

    return JsonResponse({'list': ans})
