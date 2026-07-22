from django.urls import path
from . import views


urlpatterns = [
    path('', views.approve_events, name='approve_events'),
    path('approve/<int:event_id>/', views.approve_event, name='approve_event'),
    path('reject/<int:event_id>/', views.reject_event, name='reject_event'),
]