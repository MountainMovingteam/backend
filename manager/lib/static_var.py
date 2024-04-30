RATIO_NUM = 50
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


