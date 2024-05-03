XLSX_NAME = 0
XLSX_NUM = 1
XLSX_TAG = 2
XLSX_SCHOOL = 3
XLSX_WEEKDAY = 4
XLSX_TIME = 5

XLSX_TAG_MAP = {
    '入门': 0,
    '熟练': 1
}
XLSX_WEEKDAY_MAP = {
    '周一': 0,
    '周二': 1,
    '周三': 2,
    '周四': 3,
    '周五': 4,
    '周六': 5,
    '周日': 6,
}
XLSX_SCHOOL_MAP = {
    '学院路': 0,
    '沙河': 1
}
XLSX_TIME_MAP = {
    '8:00 ~ 9:30': 1,
    '10:00 ~ 11:30': 2,
    '14:00 ~ 15:30': 3,
    '16:00 ~ 17:30': 4
}

DAY_TIME_NUM = 4  # 一天有多少个时段
WEEK_TIME_NUM = 28  # 一周总共有多少个时段

RATIO_NUM = 50

PLACE_CAPACITY = 20  # 场地的最大容量
WEEK_NUM = 16  # 一个学期有多少周
TIMR_INDEX_NUM = 56  # 一周最大的时段数量
HTTP_AUTHORIZATION = 'HTTP_AUTHORIZATION'
ADMIN_ROLE = 1
STUDENT_ROLE = 0
CURRENT_WEEK = 0
NEXT_WEEK = 1
SINGLE_ORDER = 'single'
TEAM_ORDER = 'team'
OFFICIAL_EMAIL = '3462515832@qq.com'
PASSWORD = 'mydnvlynjrabciih'
EMAIL_SUBJECT = '来自安全协会的一个短信'
QQ_SMTP_SERVER = "smtp.qq.com"
QQ_PORT = 587
ADMIN_AUTH_STR = """
token = request.META.get(HTTP_AUTHORIZATION)
if len(token) == 0 and response is None:
    response =  none_token()
    print(response)

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
"""

if __name__ == '__main__':
    print(ADMIN_AUTH_STR)
