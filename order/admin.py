from django.contrib import admin

# Register your models here.

from .models import Place, Order, Team, TeamMember

admin.site.register(Place)
admin.site.register(Order)
admin.site.register(Team)
admin.site.register(TeamMember)



