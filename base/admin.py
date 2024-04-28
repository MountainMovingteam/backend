from django.contrib import admin

# Register your models here.
from .models import Student, Admin, Notification, Picture, Push

admin.site.register(Student)
admin.site.register(Admin)
admin.site.register(Notification)
admin.site.register(Push)
admin.site.register(Picture)
