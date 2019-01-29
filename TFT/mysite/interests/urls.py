from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('favorites/', views.interests, name='favorites'),
    path('choose_and_edit_interests/', views.choose_and_edit_interests, name='choose_and_edit_interests'),

]