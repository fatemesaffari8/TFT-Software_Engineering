from django.conf.urls import url
from django.urls import path


from . import views

urlpatterns = [
    path('add_center/', views.add_center, name='add_center'),
    path('add_discount/', views.AddDiscount, name='add_discount'),
    path('centers/', views.show_centers, name='centers'),

]