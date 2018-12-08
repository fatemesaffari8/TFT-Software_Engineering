from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('add_center/', views.add_center, name='add_center'),
    path('favorites/', views.interests, name='favorites'),
    path('choose_interests/', views.choose_interests, name='choose_interests'),
    path('choose_interests/interests/', views.choose_interests, name='interests'),
    path('choose_interests_action/', views.get_interest_data, name='choose_interests_action'),
    path('centers/', views.show_centers, name='centers'),
]