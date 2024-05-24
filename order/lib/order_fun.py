import datetime

from order.models import Order
from base.models import Student, Admin, Notification
from manager.lib.static_response import *


def reject_order(reason, order_id, admin):
    # 驳回order并增加通知
    response = None
    order = Order.objects.filter(id=order_id).first()
    if order is None:
        response = order_not_exists()
        return response

    user = Student.objects.filter(student_id=order.user_id).first()
    if user is None:
        response = user_not_exists()
        return response

    if admin is None:
        response = role_wrong()
        return response

    order.status = 1
    order.save()

    count = Notification.objects.count()
    print(datetime.datetime.now())
    Notification.objects.create(notification_id=count + 1, student=user, admin=admin, reason=reason, read=False,
                                time_slot=datetime.datetime.now().strftime("%Y-%m-%d"))
    return response
