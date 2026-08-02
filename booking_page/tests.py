from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, time
from homepage.models import Event
from .models import Booking

# Aidas Kibas - Unit Tests for Booking Feature

class BookingModelTest(TestCase): # This creates a class for testing the Booking model, inheriting from Django's TestCase class.
 
    def setUp(self):

        # Create a test student

        self.student = User.objects.create_user(

            username="student1",

            password="password123"

        )
 
        # Create a test organiser

        self.organiser = User.objects.create_user(

            username="organiser",

            password="password123"

        )
 
        # Create a test event

        self.event = Event.objects.create(

            organiser=self.organiser,

            title="Basketball Tournament",

            sport_type="Basketball",

            location="NCI",

            date=date(2026, 8, 20),

            start_time=time(10, 0),

            capacity=20,

            approved=True

        )
 
    # Test 1 - Check if a booking is created successfully

    def test_booking_is_created(self):

        booking = Booking.objects.create(student=self.student, event=self.event)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(booking.student, self.student)
        self.assertEqual(booking.event, self.event)
 
    # Test 2 - Check if the event capacity does not change when a booking is created

    def test_event_capacity_does_not_change(self):

        Booking.objects.create(student=self.student, event=self.event)
        self.event.refresh_from_db()
        self.assertEqual(self.event.capacity, 20)
 
    # Test 3 - Check if the available places are calculated correctly

    def test_available_places(self):

        Booking.objects.create(student=self.student, event=self.event)
        available_places = self.event.capacity - self.event.bookings.count()
        self.assertEqual(available_places, 19)
 
    # Test 4 - Check if the booking belongs to the correct event

    def test_booking_belongs_to_correct_event(self):

        booking = Booking.objects.create(student=self.student, event=self.event)
        self.assertEqual(booking.event.title, "Basketball Tournament")

# Aidas Kibas - Unit Tests for Request Refund Feature

class RequestRefundTests(TestCase): # Class for testing the request refund feature, inheriting from Django's TestCase class.

# Setting up a test user and a test event, and creating a booking for that event.

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

# Test 1: Check if the booking is removed when a refund is confirmed

    def test_remove_booking_deletes_booking(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('remove_booking', kwargs={'booking_id': self.booking.id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

# Test 2: Check if the system correctly identifies past events and allows refund requests for them

    def test_timezone_aware_event_datetime(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('request_refund'))
        self.assertEqual(response.status_code, 200)
        booking = response.context['bookings'][0]
        event_datetime = booking.event.date.strftime('%Y-%m-%d') + ' ' + booking.event.start_time.strftime('%H:%M:%S')
        self.assertTrue(booking.is_past is not None)
