from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('center_actions_and_details/', views.centerRate, name='center_actions_and_details'),

]
