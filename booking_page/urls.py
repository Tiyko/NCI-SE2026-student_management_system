from django.urls import path
from . import views

urlpatterns = [
    path('<int:event_id>/', views.booking_page, name='booking_page'),
]