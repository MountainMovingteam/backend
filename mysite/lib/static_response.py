from django.http import JsonResponse, HttpResponse


def success_respond():
    return JsonResponse({'success': True}, status=200)


def role_wrong():
    return JsonResponse(
        {'success': False, 'reason': 'role wrong'},
        status=404)


def none_token():
    return JsonResponse({'success': False, 'reason': 'none token'}, status=404)


def login_timeout():
    return JsonResponse({'success': False, 'reason': 'login timeout'}, status=404)


def user_not_exists():
    return JsonResponse({'success': False, 'reason': 'user not exists'}, status=404)


def user_has_exists():
    return JsonResponse({'success': False, 'reason': 'user has existed'}, status=404)


def password_not_match():
    return JsonResponse({'success': False, 'reason': 'passwords do not match'}, status=404)


def place_not_exists():
    return JsonResponse({'success': False, 'reason': 'place not exists'}, status=404)


def place_full():
    return JsonResponse({'success': False, 'reason': 'place is full'}, status=404)


def place_has_group():
    return JsonResponse({'success': False, 'reason': 'This session has already been booked by a group'}, status=404)


def order_not_exists():
    return JsonResponse({'success': False, 'reason': 'order not exists'}, status=404)


def order_has_expired():
    return JsonResponse({'success': False, 'reason': 'order has expired'}, status=404)


def order_type_wrong():
    return JsonResponse({'success': False, 'reason': 'order type is wrong'}, status=404)


def lecturer_has_exists():
    return JsonResponse({'success': False, 'reason': 'lecturer has exists'}, status=404)


def lecturer_not_exists():
    return JsonResponse({'success': False, 'reason': 'lecturer not exists'}, status=404)


def lecturer_file_is_none():
    return JsonResponse({'success': False, 'reason': 'lecturer file not exists'}, status=404)


def week_num_illegal():
    return JsonResponse({'success': False, 'reason': 'week num is illegal'}, status=404)


def time_index_illegal():
    return JsonResponse({'success': False, 'reason': 'time index is illegal'}, status=404)


def necessary_content_is_none(name):
    return JsonResponse({'success': False, 'reason': f'necessary {name} is none'}, status=404)


def problem_id_not_exists():
    return JsonResponse({'success': False, 'reason': 'problem_id not exists'}, status=404)


def send_error():
    return JsonResponse({'success': False, 'reason': 'send e_mail error'}, status=404)


def verify_error():
    return JsonResponse({'success': False, 'reason': 'e_mail code wrong'}, status=404)


def excel_error():
    return JsonResponse({'success': False, 'reason': 'excel error'}, status=404)
