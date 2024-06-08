import base64
import os.path
import random
import re
import string
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from django.http import JsonResponse
from django.core.mail import send_mail
import json
from .models import Student, Admin, Notification, Picture, Push, EmailVerify
import datetime
import jwt
from mysite.lib.static_fun import *
from mysite.lib.static_response import *
from django.core.files.storage import FileSystemStorage
from order.models import Order
from mysite.lib.static_fun import admin_auth
from mysite import settings


# Create your views here.

def login(request):
    data = json.loads(request.body.decode('utf-8'))
    user_id = data['id']
    password = rsa_decode(data['password'])
    user = Student.objects.filter(student_id=user_id).first()
    login_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if user:
        if user.password != password:
            return password_not_match()

        token = jwt.encode({'id': data['id'], 'login_time': login_time, 'role': 0}, 'secret_key', algorithm='HS256',
                           headers=headers).decode('ascii')
        rep = JsonResponse({
            'token': token,
            'role': 0
        })
        return rep
    else:
        user = Admin.objects.filter(staff_id=user_id).first()
        if user:
            if user.password != password:
                return password_not_match()

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
    response = check_attribute(data['id'], 'id')
    if response is not None:
        return response

    if Student.objects.filter(student_id=data['id']) or Admin.objects.filter(staff_id=data['id']):
        return user_has_exists()

    password = rsa_decode(data['password'])
    response = check_attribute(password, 'password')
    if response is not None:
        return response

    email = data['email']
    response = check_attribute(email, 'email')
    if response is not None:
        return response

    email_code = data['email_code']
    verify = EmailVerify.objects.filter(email=email, code=email_code).first()

    if not verify:
        return verify_error()

    if data['phone'] is not None:
        response = check_attribute(data['phone'], 'phone')
        if response is not None:
            return response

    Student.objects.create(student_id=data['id'],
                           name=data['name'],
                           email=email,
                           phone=data['phone'],
                           academy=data['academy'],
                           password=password)
    verify.delete()
    token = jwt.encode(
        {'id': data['id'], 'login_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'role': 0},
        'secret_key', algorithm='HS256', headers=headers).decode('ascii')
    rep = JsonResponse({
        'token': token,
        'role': 0
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
    old_password = rsa_decode(data['old_password'])
    password = rsa_decode(data['password'])

    if user.password != old_password:
        return password_not_match()

    response = check_attribute(password, 'password')
    if response is not None:
        return response

    user.password = password
    user.save()
    return success_respond()


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
            'key_words': no.reason,
            'type': no.type,
            'status': no.read
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
    if no.type == 0:
        content = "抱歉，因为" + no.reason + ",您的参观请求已被驳回"
    else:
        content = "您有近期的体验馆预约，请及时参加"
    return JsonResponse({
        'time': no.time_slot,
        'content': content,
        'key_word': no.reason
    })


def notice_read(request):
    response = user_auth(request)
    if response is not None:
        return response

    data = json.loads(request.body.decode('utf-8'))
    no = Notification.objects.filter(notification_id=data['notification_id']).first()
    if no is not None:
        no.read = 1
        no.save()
        return success_respond()
    return notification_not_exists()


def notice_delete(request):
    response = user_auth(request)
    if response is not None:
        return response

    data = json.loads(request.body.decode('utf-8'))
    no = Notification.objects.filter(notification_id=data['notification_id']).first()
    if no is not None:
        no.delete()
        return success_respond()
    return notification_not_exists()


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

    print(request)

    new_id = request.POST['id']
    response = check_attribute(new_id, 'id')
    if new_id != "":
        if response is not None:
            return response
        if Student.objects.filter(student_id=new_id) or Admin.objects.filter(staff_id=new_id):
            return user_has_exists()

    name = request.POST['name']

    phone = request.POST['phone']
    response = check_attribute(phone, 'phone')
    if phone != "" and response is not None:
        return response

    academy = request.POST['academy']
    response = check_attribute(academy, 'academy')
    if academy != "" and response is not None:
        return response

    if request.FILES.get('avatar', None):
        avatar = request.FILES['avatar']
        filename = fs.save(id, avatar)
        user.avatar = filename
    if role == 0:
        if id:
            user.student_id = id
        if name:
            user.name = name
        if phone:
            user.phone = phone
        if academy:
            user.academy = academy
    elif role == 1:
        if id:
            user.staff_id = id
        if name:
            user.name = name
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


def check_attribute(str, type):
    if type != "password" and type != "id":
        if str == "":
            return None
    if type == "password":
        if re.search("^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$", str) is None:
            return JsonResponse({
                'success': False,
                'reason': '密码需要包含数字和字母，且为6~16位'
            }, status=404)
    elif type == "email":
        if re.search("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", str) is None:
            return JsonResponse({
                'success': False,
                'reason': '邮箱格式错误'
            }, status=404)
    elif type == "phone":
        if re.search("^\\d{11}$", str) is None:
            return JsonResponse({
                'success': False,
                'reason': '电话格式错误'
            }, status=404)
    elif type == "id":
        if re.search("^(\d{8}|[A-Za-z]{2}\d{7})$", str) is None:
            return JsonResponse({
                'success': False,
                'reason': '学工号格式错误'
            }, status=404)
    # elif type == 'academy':
    #     if len(str.toString()) > 2:
    #         return JsonResponse({
    #             'success': False,
    #              'reason': '学院号错误'
    #          }, status=404)
    return None


def get_public_key(request):
    # print(settings.public_key)
    return JsonResponse({
        'public_key': settings.public_key.decode()
    })


def send_message(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data['email']
    response = check_attribute(email, 'email')
    if response is not None:
        return response

    code = generate_random_string()

    title = "体验馆预约账号激活"
    body = "您的邮箱注册验证码为：{0},请及时验证".format(code)
    status = send_mail(title, body, settings.EMAIL_FROM, [email])
    if not status:
        return send_error()
    #if EmailVerify.objects.count() != 0:
    #    EmailVerify.objects.filter(email=email).delete()
    verify = EmailVerify()
    verify.email = email
    verify.code = code
    verify.save()
    return success_respond()


def password_encode(request):
    data = json.loads(request.body.decode('utf-8'))
    encoded_password = rsa_encode(data['password'])
    return JsonResponse({
        'encoded_password': encoded_password
    })


def rsa_decode(str):
    print(str, type(str))
    rsa_prk = RSA.importKey(settings.private_key)
    rsa = PKCS1_v1_5.new(rsa_prk)
    res = rsa.decrypt(base64.b64decode(str), None).decode('utf-8')
    print(res, type(res))
    return res


def rsa_encode(str):
    print(str, type(str))
    rsa_pk = RSA.importKey(settings.public_key)
    rsa = PKCS1_v1_5.new(rsa_pk)
    res = rsa.encrypt(str.encode('utf-8'))
    res = base64.b64encode(res).decode('utf-8')
    print(res, type(res))
    return res


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
        is_expired, order_json = get_order_log_json(order)
        if not is_expired:
            ans.append(order_json)

    return JsonResponse({'list': ans})
