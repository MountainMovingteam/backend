from django.http import JsonResponse, HttpResponse


def success_respond():
    return JsonResponse({'success': True})


def role_wrong():
    return JsonResponse({'success': False})


def none_token():
    return JsonResponse({'success': False})


def login_timeout():
    return JsonResponse({'success': False})


def user_not_exists():
    return JsonResponse({'success': False})


def place_not_exists():
    return JsonResponse({'success': False})


def order_not_exists():
    return JsonResponse({'success': False})


def order_type_wrong():
    return JsonResponse({'success': False})


def lecturer_has_exists():
    return JsonResponse({'success': False})


def lecturer_not_exists():
    return JsonResponse({'success': False})
