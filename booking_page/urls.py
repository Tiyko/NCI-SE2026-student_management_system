from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
     path('', views.booking_page, name='booking_page')
]
