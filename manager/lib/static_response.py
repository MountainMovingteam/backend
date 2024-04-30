from django.http import JsonResponse, HttpResponse


def success_respond():
    return JsonResponse({'success': True}, status=200)


def role_wrong():
    return JsonResponse({'success': False}, status=404)


def none_token():
    return JsonResponse({'success': False}, status=404)


def login_timeout():
    return JsonResponse({'success': False}, status=404)


def user_not_exists():
    return JsonResponse({'success': False}, status=404)


def place_not_exists():
    return JsonResponse({'success': False}, status=404)


def order_not_exists():
    return JsonResponse({'success': False}, status=404)


def order_type_wrong():
    return JsonResponse({'success': False}, status=404)


def lecturer_has_exists():
    return JsonResponse({'success': False}, status=404)


def lecturer_not_exists():
    return JsonResponse({'success': False}, status=404)
