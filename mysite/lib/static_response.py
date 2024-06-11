from django.http import JsonResponse, HttpResponse


def success_respond():
    return JsonResponse({'success': True}, status=200)


def role_wrong():
    return JsonResponse(
        {'success': False, 'reason': '身份错误'},
        status=404)


def none_token():
    return JsonResponse({'success': False, 'reason': '无token'}, status=404)


def login_timeout():
    return JsonResponse({'success': False, 'reason': '登录超时'}, status=404)


def user_not_exists():
    return JsonResponse({'success': False, 'reason': '用户不存在'}, status=404)


def user_has_exists():
    return JsonResponse({'success': False, 'reason': '该用户已存在'}, status=404)


def password_not_match():
    return JsonResponse({'success': False, 'reason': '密码错误'}, status=404)


def place_not_exists():
    return JsonResponse({'success': False, 'reason': '该场次不存在'}, status=404)


def place_full():
    return JsonResponse({'success': False, 'reason': '该场次已满'}, status=404)


def place_has_group():
    return JsonResponse({'success': False, 'reason': '该场次已有团体预约'}, status=404)


def order_not_exists():
    return JsonResponse({'success': False, 'reason': '预约记录不存在'}, status=404)


def order_has_expired():
    return JsonResponse({'success': False, 'reason': '预约已过期'}, status=404)


def order_type_wrong():
    return JsonResponse({'success': False, 'reason': '预约类型错误'}, status=404)


def lecturer_has_exists():
    return JsonResponse({'success': False, 'reason': '该讲解员已存在'}, status=404)


def lecturer_not_exists():
    return JsonResponse({'success': False, 'reason': '讲解员不存在'}, status=404)


def lecturer_file_is_none():
    return JsonResponse({'success': False, 'reason': '讲解员文件不存在'}, status=404)


def week_num_illegal():
    return JsonResponse({'success': False, 'reason': 'week num非法'}, status=404)


def time_index_illegal():
    return JsonResponse({'success': False, 'reason': 'time index非法'}, status=404)


def necessary_content_is_none(name):
    return JsonResponse({'success': False, 'reason': f'必要信息{name}为空'}, status=404)


def problem_id_not_exists():
    return JsonResponse({'success': False, 'reason': 'problem_id不存在'}, status=404)


def send_error():
    return JsonResponse({'success': False, 'reason': '发送邮件错误'}, status=404)


def verify_error():
    return JsonResponse({'success': False, 'reason': '邮箱验证码错误'}, status=404)


def excel_error():
    return JsonResponse({'success': False, 'reason': '上传的excel有误'}, status=404)


def notification_not_exists():
    return JsonResponse({'success': False, 'reason': '该通知不存在'}, status=404)
