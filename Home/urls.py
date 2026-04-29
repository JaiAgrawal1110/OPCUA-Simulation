from django.contrib import admin
from django.urls import path
from Home import views

urlpatterns = [
    path("", views.index, name='Home'),
    path("About_us/", views.About_us, name='About_us'),
    path("Contacts/", views.Contacts, name='Contacts'),
    path("OPC_UA/", views.OPC_UA, name='OPC UA'),
    path('start_transfer/', views.start_transfer, name='Start Transfer'),
    path('stop_transfer/', views.stop_transfer, name='Stop Transfer'),
    path('start_mysql_transfer/', views.start_mysql_transfer, name='Start MySQL Transfer'),
    path('stop_mysql_transfer/', views.stop_mysql_transfer, name='Stop MySQL Transfer'),
    path('show_data/', views.show_data, name='Show Data'),
    path('hide_data/', views.hide_data, name='Hide Data'),
    path('filtered_data/', views.filtered_data, name='filtered_data')
]
