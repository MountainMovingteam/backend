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
ADMIN_AUTH_STR = '''
    token = request.META.get(HTTP_AUTHORIZATION)
    if not token:
        return none_token()

    id, role, is_login = check_token(token)

    if not is_login:
        return login_timeout()

    if role != ADMIN_ROLE:
        return role_wrong()

    user = get_user(id, role)

    if user is None:
        return user_not_exists()
'''
