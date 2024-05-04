from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import jwt
import datetime
from .lib.static_fun import *
from .lib.static_var import *
from .lib.static_response import *
from .models import LecturerPlace, Lecturer
from order.lib.time import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import openpyxl


# Create your views here.


def query_place(request):
    response = admin_auth(request)

    if response is not None:
        return response

    place_info_array = []
    # 只看这一周和下一周的内容
    current_week_num = get_week_num()
    current_week_place = Place.objects.filter(week_num=current_week_num)
    next_week_place = Place.objects.filter(week_num=current_week_num + 1)

    for place in current_week_place:
        place_info = gen_place_json(place)
        place_info['week_num'] = CURRENT_WEEK
        place_info_array.append(place_info)

    for place in next_week_place:
        place_info = gen_place_json(place)
        place_info['week_num'] = NEXT_WEEK
        place_info_array.append(place_info)

    return JsonResponse({
        'place_details': place_info_array
    })


def query_order(request):
    response = admin_auth(request)

    if response is not None:
        return response

    data = json.loads(request.body.decode('utf-8'))

    week_num = data.get('week_num', None)
    time_index = data.get('time_index', None)

    if week_num is None or time_index is None:
        return place_not_exists()

    if week_num < 0 or week_num > WEEK_NUM:
        return week_num_illegal()

    if time_index < 0 or time_index > TIMR_INDEX_NUM:
        return time_index_illegal()

    week_num = week_num + get_week_num()

    place = Place.objects.filter(week_num=week_num, time_index=time_index).first()
    orders = Order.objects.filter(place=place)

    order_json_array = []
    for order in orders:
        order_json_array.append(gen_order_json(order))

    return JsonResponse({
        'list': order_json_array
    })


def query_team_order(request):
    response = admin_auth(request)

    if response is not None:
        return response

    data = json.loads(request.body.decode('utf-8'))

    order_id = data.get('order_id', None)

    if order_id is None:
        return order_not_exists()

    order = Order.objects.filter(id=order_id).first()

    if order is None:
        return order_not_exists()

    if order.is_person:
        return order_type_wrong()

    return gen_order_json(order)


def reject_application(request):
    response = admin_auth(request)

    if response is not None:
        return response
    data = json.loads(request.body.decode('utf-8'))

    option = data['option']
    order_id = data['order_id']

    if order_id is None:
        return order_not_exists()

    order = Order.objects.filter(id=order_id).first()

    if order is None:
        return order_not_exists()

    user_id = order.user_id
    user = Student.objects.filter(student_id=user_id).first()

    if user is None:
        return user_not_exists()

    receive_email = user.email

    sender_email = OFFICIAL_EMAIL

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receive_email
    message['Subject'] = EMAIL_SUBJECT

    body = option

    message.attach(MIMEText(body, 'plain'))

    smtp_server = QQ_SMTP_SERVER

    port = QQ_PORT

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, PASSWORD)
        text = message.as_string()
        server.sendmail(sender_email, receive_email, text)
    except Exception as e:
        print("error in reject")
    finally:
        server.quit()
    return success_respond()


def query_all_lecturer(request):
    response = admin_auth(request)

    if response is not None:
        return response
    return get_lecturer_json_array(Lecturer.objects.all())


def query_lecturer(request):
    response = admin_auth(request)

    if response is not None:
        return response
    data = json.loads(request.body.decode('utf-8'))
    tags = data.get('tags', None)
    content = data.get('content', None)

    tags_set = query_lecturer_accord_tags(tags)
    content_set = query_lecturer_accord_content(content)

    return get_lecturer_json_array(tags_set & content_set)


def modify_lecture_info(request):
    response = admin_auth(request)

    if response is not None:
        return response
    data = json.loads(request.body.decode('utf-8'))
    old_lecturer_id = data['old_num']

    if Lecturer.objects.filter(lecturer_id=old_lecturer_id).first() is None:
        return lecturer_not_exists()

    old_lecturer = Lecturer.objects.filter(lecturer_id=old_lecturer_id).first()


    new_lecturer_id = data['num']
    name = data['name']
    tag = data['tag']
    time_index = data['time_index']

    if new_lecturer_id != old_lecturer_id and Lecturer.objects.filter(lecturer_id=new_lecturer_id).first() is not None:
        return lecturer_has_exists()

    old_lecturer.delete()

    Lecturer.objects.create(lecturer_id=new_lecturer_id, name=name, tag=tag)

    assign_lecture_session(lecture_id=new_lecturer_id, time_index=time_index)

    return success_respond()


def add_lecturer(request):
    response = admin_auth(request)

    if response is not None:
        return response
    data = json.loads(request.body.decode('utf-8'))
    lecturer_id = data['num']
    name = data['name']
    tag = data['tag']

    if len(Lecturer.objects.filter(lecturer_id=lecturer_id)) == 0:
        Lecturer.objects.create(lecturer_id=lecturer_id, name=name, tag=tag)

    time_index = data['time_index']

    if time_index is None:
        return success_respond()

    assign_lecture_session(lecturer_id, time_index)
    return success_respond()


def delete_lecturer(request):
    response = admin_auth(request)

    if response is not None:
        return response

    data = json.loads(request.body.decode('utf-8'))
    lecturer = Lecturer.objects.filter(lecturer_id=data['num']).first()

    if lecturer is not None:
        lecturer.delete()

    return success_respond()


def delete_all_lecturer(request):
    response = admin_auth(request)

    if response is not None:
        return response

    Lecturer.objects.all().delete()

    return success_respond()


def lecturer_file_upload(request):
    response = admin_auth(request)

    if response is not None:
        return response

    uploaded_file = request.FILES.get("file")
    print(uploaded_file)
    if uploaded_file is None:
        return lecturer_file_is_none()

    workbook = openpyxl.load_workbook(uploaded_file)
    worksheet = workbook.active
    new_lecturer_list = []
    for row in worksheet.iter_rows(values_only=True):
        if row[XLSX_NAME] == '姓名':
            continue

        name = row[XLSX_NAME]
        num = row[XLSX_NUM]
        tag = XLSX_TAG_MAP[row[XLSX_TAG]]
        if Lecturer.objects.filter(lecturer_id=num).first() is None:
            Lecturer.objects.create(lecturer_id=num, name=name, tag=tag)

        new_lecturer_list.append(Lecturer.objects.filter(lecturer_id=num).first())
        time_index = time2time_index(row[XLSX_SCHOOL], row[XLSX_WEEKDAY], row[XLSX_TIME])
        assign_lecture_session(num, time_index)

    return get_lecturer_json_array(new_lecturer_list)
