from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('favorites/', views.interests, name='favorites'),
    path('choose_interests/', views.choose_interests, name='choose_interests'),
    path('choose_interests/interests/', views.choose_interests, name='interests'),
    path('choose_interests_action/', views.get_interest_data, name='choose_interests_action'),

]