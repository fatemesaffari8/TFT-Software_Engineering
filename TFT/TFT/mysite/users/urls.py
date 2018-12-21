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
    path('suggesting_centers/', views.suggest_centers, name='suggesting_centers'),
    path('add_discount/', views.AddDiscount, name='add_discount'),
    path('suggest_Package/', views.suggestPackage, name='suggest_Package'),
    path('suggesting_Package/', views.suggestPackage, name='suggesting_Package'),
    path('center_actions_and_details/', views.centerRate, name='center_actions_and_details'),

]
