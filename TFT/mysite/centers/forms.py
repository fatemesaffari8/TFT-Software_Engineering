
from django import forms

from .models import Center


class AddCenter(forms.ModelForm):
    class Meta:
        model = Center
        fields = '__all__'