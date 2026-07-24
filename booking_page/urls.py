from django.urls import path
from . import views

urlpatterns = [
    path('<int:event_id>/', views.booking_page, name='booking_page'),
    path("request_refund/", views.request_refund, name="request_refund"),
]