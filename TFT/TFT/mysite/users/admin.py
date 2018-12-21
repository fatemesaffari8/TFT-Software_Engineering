from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import (Center, CenterHours, CustomUser, Interest, ManagerCenters,
                     UserInterests)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserInterests)
admin.site.register(Interest)
admin.site.register(Center)
admin.site.register(ManagerCenters)
admin.site.register(CenterHours)
