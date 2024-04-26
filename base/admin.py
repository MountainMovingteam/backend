from django.contrib import admin

# Register your models here.
from .models import Student, Admin

admin.site.register(Student)
admin.site.register(Admin)