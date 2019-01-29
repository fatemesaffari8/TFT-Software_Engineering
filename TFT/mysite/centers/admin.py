from django.contrib import admin

from centers.models import Center, ManagerCenters, CenterHours

admin.site.register(Center)
admin.site.register(ManagerCenters)
admin.site.register(CenterHours)
