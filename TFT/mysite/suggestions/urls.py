from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('suggesting_centers/', views.suggest_centers, name='suggesting_centers'),
    path('suggest_Package/', views.suggestPackage, name='suggest_Package'),
    path('suggesting_Package/', views.suggestPackage, name='suggesting_Package'),

]
