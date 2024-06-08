from time import sleep, time
from celery import shared_task
from order.models import Place, Order
from base.models import Notification, Student
from mysite.lib.time import *


@shared_task(bind=True)
def order_remind():
    print("order_remind_begin")
    week_num = get_week_num()
    week_day = (get_week_day() + 1) % 7
    if get_week_day() + 1 == 7:
        week_num = week_num + 1

    w = 4 * week_day
    time_index_range = [w + 1, w + 2, w + 3, w + 4, w + 29, w + 30, w + 31, w + 32]
    places = Place.objects.filter(week_num=week_num, time_index__range=time_index_range).all()
    orders = Order.objects.filter(place__in=places)
    for order in orders:
        user = Student.objects.filter(id=order.student_id).first()
        count = Notification.objects.count()
        Notification.objects.create(notification_id=count + 1, student=user, reason="预约提醒",
                                    time_slot=datetime.datetime.now().strftime("%Y-%m-%d"))
    print("order_remind_finish")
