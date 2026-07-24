from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from homepage.models import Event
from .models import Booking


class RequestRefundTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='password')
        self.organizer = User.objects.create_user(username='organizer', password='password')
        self.event = Event.objects.create(
            organiser=self.organizer,
            title='Test Event',
            sport_type='Football',
            location='Campus',
            date='2026-01-01',
            start_time='10:00:00',
            capacity=50,
            approved=True,
        )
        self.booking = Booking.objects.create(student=self.user, event=self.event)

    def test_request_refund_shows_confirmation_message(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('request_refund'), {'booking_id': self.booking.id})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure you want to request a refund')
        self.assertTrue(Booking.objects.filter(id=self.booking.id).exists())

    def test_confirm_refund_deletes_booking_and_shows_success_message(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('request_refund'),
            {'booking_id': self.booking.id, 'confirm_refund': '1'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())
        self.assertContains(response, 'Your refund has been processed')
        self.assertContains(response, 'You currently have no bookings.')
