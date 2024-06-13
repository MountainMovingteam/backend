import jwt
from base.models import Student, Admin
from manager.models import Lecturer, LecturerPlace
from order.models import Order, TeamMember
from mysite.lib.time import *
from order.models import Place
from rapidfuzz import fuzz
from .static_var import *
from .static_response import *
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def admin_auth(request):
    response = None
    token = request.META.get(HTTP_AUTHORIZATION)
    if token is None or len(token) == 0:
        response = none_token()

    if response is None:
        id, role, is_login = check_token(token)

    if response is None and not is_login:
        response = login_timeout()

    if response is None and role != ADMIN_ROLE:
        response = role_wrong()

    if response is None:
        user = get_user(id, role)

    if response is None and user is None:
        response = user_not_exists()

    return response


def user_auth(request):
    response = None
    token = request.META.get(HTTP_AUTHORIZATION)
    if token is None or len(token) == 0:
        response = none_token()

    if response is None:
        id, role, is_login = check_token(token)

    if response is None and not is_login:
        response = login_timeout()

    if response is None:
        user = get_user(id, role)

    if response is None and user is None:
        response = user_not_exists()

    return response


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


def assign_lecture_session(lecture_id, time_index):
    lecturer = Lecturer.objects.filter(lecturer_id=lecture_id).first()
    current_week_num = get_week_num()
    # 从当前周到16周指定这个讲解人
    for i in range(current_week_num, 17):
        week_num = i
        place = Place.objects.filter(week_num=week_num, time_index=time_index).first()
        if LecturerPlace.objects.filter(lecturer=lecturer, place=place).first() is None:
            LecturerPlace.objects.create(lecturer=lecturer, place=place)


def query_lecturer_accord_content(content):
    if content is None:
        return set(list(Lecturer.objects.all()))

    res_set = set()
    for lecturer in Lecturer.objects.all():
        lecturer_id = lecturer.lecturer_id
        name = lecturer.name
        if fuzz.ratio(lecturer_id, content) >= RATIO_NUM:
            res_set.add(lecturer)
        if fuzz.ratio(name, content) >= RATIO_NUM:
            res_set.add(lecturer)

    return res_set


'''
tags是一个数组
11-12：分别代表入门和熟练
21-25：代表周一到周五
31-34：代表四个场次时间段
31：8：00-9：30
32：10：00-11：30
33：14：00-15：30
34：16：00-17：30
'''


def query_lecturer_accord_tags(tags):
    if tags is None or len(tags) == 0:
        return set(list(Lecturer.objects.all()))

    profi_set = set()
    profi_flag = 0
    weekday_set = set()
    weekday_flag = 0
    session_set = set()
    session_flag = 0
    for tag in tags:

        if tag // 10 == 1:
            profi_flag = 1
            prof = tag % 10 - 1
            profi_set = profi_set.union(query_lecturer_accord_profi(prof))

        if tag // 10 == 2:
            weekday_flag = 1
            weekday = tag % 10
            weekday_set = weekday_set | query_lecturer_accord_weekday(weekday)
        if tag // 10 == 3:
            session_flag = 1
            session = tag % 10
            session_set = session_set | query_lecture_accord_session(session)

    if profi_flag == 0:
        profi_set = set(list(Lecturer.objects.all()))
    if weekday_flag == 0:
        weekday_set = set(list(Lecturer.objects.all()))

    if session_flag == 0:
        session_set = set(list(Lecturer.objects.all()))

    return profi_set & weekday_set & session_set


def query_lecturer_accord_profi(profi):
    lecturer_set = set()
    for lecturer in Lecturer.objects.all():
        if lecturer.tag == profi:
            lecturer_set.add(lecturer)

    return set(list(lecturer_set))


def query_lecturer_accord_weekday(weekday):
    lecturer_set = set()
    for lecturerPlace in LecturerPlace.objects.all():
        place = lecturerPlace.place
        time_index = place.time_index
        place_weekday = time_index2weekday(time_index)
        if place_weekday == weekday:
            lecturer_set.add(lecturerPlace.lecturer)

    return lecturer_set


def query_lecture_accord_session(session):
    lecturer_set = set()
    for lecturerPlace in LecturerPlace.objects.all():

        place = lecturerPlace.place
        time_index = place.time_index
        place_session = time_index2session(time_index)
        if place_session == session:
            lecturer_set.add(lecturerPlace.lecturer)

    return lecturer_set


def time_index2weekday(time_index):
    return (time_index % 28) // 4 + 1


def time_index2session(time_index):
    return time_index % 5


def get_lecturer_json_array(lecturer_set):
    lecturer_json_array = []
    for lecturer in lecturer_set:
        lecturer_json_array.append(gen_lecturer_json(lecturer))

    return JsonResponse({
        'list': lecturer_json_array
    })


def gen_lecturer_json(lecturer):
    place_array = set()
    for lecturerPlace in LecturerPlace.objects.filter(lecturer=lecturer):
        place = lecturerPlace.place
        place_array.add(place.time_index)

    return {
        'num': lecturer.lecturer_id,
        'name': lecturer.name,
        'tag': lecturer.tag,
        'time_index': list(place_array)
    }


'''
字段含义： place_details ：
表示场地信息，为一个数组。
week_num:表示是第几周 
time_index：给每一个时间段编号，共有56个编号，1-28代表学院路，29-56代表沙河。
1-4代表周一的四个时间段，5-8代表周二的四个时间段，以此类推。 
capacity：代表该时间段的容量。 
enrolled：已选人数。 
lecturer：讲师的名字。若为空，代表没有。 
type：预约情况，0代表一个人都没有预约，1代表有人预约但未满，2代表已满。

只传两周的内容，0代表这周，1代表下一周
'''


def gen_place_json(place):
    orders = Order.objects.filter(place=place)
    enrolled = 0
    for order in orders:
        if order.is_person:
            enrolled = enrolled + 1
        else:
            team = order.team
            team_num = TeamMember.objects.filter(team=team).count()
            enrolled = enrolled + team_num + 1

    lecturer_name_array = []
    lecturerPlaces = LecturerPlace.objects.filter(place=place)
    for lecturerPlace in lecturerPlaces:
        lecturer = lecturerPlace.lecturer
        lecturer_name_array.append(lecturer.name)

    type = 0
    if enrolled > 0 and enrolled < place.capacity:
        type = 1
    elif enrolled == place.capacity:
        type = 2

    return {
        'week_num': place.week_num,
        'time_index': place.time_index,
        'capacity': place.capacity,
        'enrolled': enrolled,
        'lecturer': lecturer_name_array,
        'type': type
    }


def gen_order_json(order):
    if order.is_person:
        order_type = SINGLE_ORDER
    else:
        order_type = TEAM_ORDER
    return {
        'order_id': order.id,
        'order_type': order_type,
        'name': order.name,
        'id': order.user_id,
        'phone': order.phone,
        'status': order.status

    }


def gen_team_order_json(order):
    team = order.team

    return {
        'leader': {
            'id': team.leader_id,
            'name': team.leader_name,
            'phone': team.leader_phone,
            'academy': team.academy
        },
        'list': gen_team_json(team)
    }


def gen_team_json(team):
    team_json_array = []
    teamMembers = TeamMember.objects.filter(team=team)
    for mem in teamMembers:
        team_json_array.append(gen_teamMem_json(mem))

    return team_json_array


def gen_teamMem_json(teamMember):
    return {
        'id': teamMember.member_id,
        'name': teamMember.member_name
    }


def time2time_index(school, weekday, time):
    return XLSX_SCHOOL_MAP[school] * WEEK_TIME_NUM + XLSX_WEEKDAY_MAP[weekday] * DAY_TIME_NUM + XLSX_TIME_MAP[time]


def time_index2fabs(week_num, time_index):
    return week_num * 56 + time_index % 28


def current_time_index():
    current_week_num = get_week_num()
    current_day_num = get_week_day()
    current_day_index = current_week_num * 56 + current_day_num * 4 - 4

    current_hour = datetime.datetime.now().hour
    current_minute = datetime.datetime.now().minute

    if current_hour >= 9 and current_hour <= 10 and current_minute >= 30:
        current_day_index = current_day_index + 1
    if current_hour >= 11 and current_hour <= 14 and current_minute >= 30:
        current_day_index = current_day_index + 2
    if current_hour >= 15 and current_hour <= 16 and current_minute >= 30:
        current_day_index = current_day_index + 3
    if current_hour >= 17 and current_minute >= 30:
        current_day_index = current_day_index + 4

    return current_day_index


def get_order_log_json(order):
    place = order.place
    if order.is_person:
        type = 0
    else:
        type = 1
    week_num = place.week_num
    time_index = place.time_index
    status = order.status
    is_expired = 0
    if current_time_index() >= time_index2fabs(week_num, time_index):
        is_expired = 1

    return is_expired, {
        'type': type,
        'week_num': week_num,
        'time_index': time_index,
        'status': status,
        'lecturers': get_lecturers_accord_place(place)
    }


def get_lecturers_accord_place(place):
    lecturers_set = set()
    for lecturerPlace in LecturerPlace.objects.filter(place=place):
        lecturer = lecturerPlace.lecturer
        lecturers_set.add(lecturer.name)

    return list(lecturers_set)


def question_json(question):
    return {
        "question_id": question.id,
        "type": question.type,
        "content": {
            "a_option": question.A_content,
            "b_option": question.B_content,
            "c_option": question.C_content,
            "d_option": question.D_content,
            "title": question.title
        }
    }


def chinese_tokenizer(text):
    # 使用 jieba 进行中文分词
    return jieba.lcut(text)


def vector_match(question, keywords):
    # 对问题和关键词进行分词
    corpus = [question] + [keywords]
    tokenized_corpus = [' '.join(chinese_tokenizer(doc)) for doc in corpus]

    # 创建 TfidfVectorizer 对象，并使用分词后的文本
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(tokenized_corpus).toarray()

    # 计算余弦相似度矩阵
    cosine_matrix = cosine_similarity(vectors)

    # 提取关键词向量的相似度分数
    keyword_scores = cosine_matrix[0, 1:]

    # 设置一个相似度阈值，比如 0.1
    return any(score > 0.1 for score in keyword_scores)
