from django.db import models
from django.conf import settings
from phone_field import PhoneField


TYPE_CHOICES = [
    ('رستوران وکافی شاپ', 'رستوران وکافی شاپ'),
    ('سینما ، کنسرت وتئاتر', 'سینما ، کنسرت وتئاتر'),
    ('شهربازی', 'شهربازی'),
    ('مرکز خرید', 'مرکز خرید'),
    ('مجموعه ورزشی', 'مجموعه ورزشی'),
    ('پارک وفضای آزاد', 'پارک وفضای آزاد'),
    ('غیره', 'غیره'),
]


class Center(models.Model):
    name = models.CharField(max_length=100, unique=False, blank=True)
    address = models.CharField(max_length=250)
    phone_number = PhoneField(blank=False, help_text='Contact phone number', default='')
    email= models.EmailField()
    type=models.CharField(max_length=100, choices=TYPE_CHOICES, default='STRING')
    ticket_cost=models.IntegerField(help_text='In Toman')
    description = models.CharField(max_length=500)
    def __str__(self):
        return self.name


class CenterHours(models.Model):
    center_id=models.ForeignKey(Center, unique=False, on_delete=models.CASCADE)
    day=models.CharField(max_length=100)
    open_time=models.CharField(max_length=100)
    close_time=models.CharField(max_length=100)



class ManagerCenters(models.Model):
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, unique=False, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, unique=True, on_delete=models.DO_NOTHING)
    def __unicode__(self):
        return self.user.username


class Discounts(models.Model):
    center_id=models.ForeignKey(Center, unique=False, on_delete=models.CASCADE)
    new_cost=models.IntegerField(help_text='In Toman')
    expiration_date=models.DateField()
    rate=models.IntegerField()
