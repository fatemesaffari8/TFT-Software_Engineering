from django.conf.urls import url
from django.urls import path


from . import views

urlpatterns = [
    path('add_center/', views.add_center, name='add_center'),
    path('add_discount/', views.AddDiscount, name='add_discount'),
    path('centers/', views.show_centers, name='centers'),
    path('find_centers/', views.find_centers, name='find_centers'),
    path('findCenterByCategory/', views.findCenterByCategory, name='findCenterByCategory'),
    path('findCenterByTime/', views.findCenterByTime, name='findCenterByTime'),
    path('centerFilters/', views.centersFilters, name='centerFilters'),

]