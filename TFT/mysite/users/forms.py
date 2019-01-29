from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Center, CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'phone_number',
                  'email','address', 'birth_date', 'gender','center_manager')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'phone_number',
                  'email','address', 'birth_date', 'gender', 'center_manager')

class AddCenter(forms.ModelForm):
    class Meta:
        model = Center
        fields = '__all__'
