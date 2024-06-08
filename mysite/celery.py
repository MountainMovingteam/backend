# from __future__ import absolute_import, unicode_literals
# import os
# import django
# from celery import Celery
# from django.conf import settings
# from base.models import Notification, Student
# from order.models import Order, Place
# from mysite.lib.time import *
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# django.setup()
#
# celery_app = Celery('mysite')
# celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


"""@app.task(bind=True)
def order_remind(self):
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
"""