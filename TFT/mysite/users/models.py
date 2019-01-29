from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phone_field import PhoneField

from interests.models import Interest

GENGER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]



class CustomUser(AbstractUser):
    address = models.CharField(max_length=60, unique=False, blank=True, help_text='Optional', default='')
    phone_number = PhoneField(blank=False, help_text='Contact phone number', default='')
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENGER_CHOICES, default='STRING')
    favorites = models.ManyToManyField(Interest, related_name='favorited_by')
    center_manager=models.BooleanField(default=False,help_text='Select if you own a center and you want to register it on our site')
    def __str__(self):
        return self.email

class UserInterests(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=False, on_delete=models.DO_NOTHING)
    interest = models.ForeignKey(Interest, unique=False, on_delete=models.DO_NOTHING)
    class Meta:
        unique_together = (("user", "interest"),)













