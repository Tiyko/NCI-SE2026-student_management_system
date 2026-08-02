from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from homepage.models import Event
from datetime import date, time

# Aidas Kibas - Unit Tests for Book Event Feature

class EventTests(TestCase):
    def setUp(self):
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

# Test 1: Check if the event is booked

    def test_event_booked(self):
        # Check if the event is booked
        self.assertTrue(self.event.approved)

# Test 2: Check if the event has no places left

    def test_no_places_left(self):
        # Check if the event has no places left
        self.event.capacity = 0
        self.event.save()
        self.assertEqual(self.event.capacity, 0)

# Test 3: Check if the event is in the past

    def test_event_in_past(self):
        # Check if the event is in the past
        self.event.date = date(2020, 7, 20)
        self.event.save()
        self.assertTrue(self.event.date < date.today())

# Aidas Kibas - Unit Tests for Create Event Feature

class CreateEventTests(TestCase):
    def setUp(self):

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
            approved=False
        )

# Test 1: Check if the event is created successfully

    def test_event_creation(self):
     
        self.assertEqual(self.event.title, "Basketball Tournament")
        self.assertEqual(self.event.sport_type, "Basketball")
        self.assertEqual(self.event.location, "NCI")
        self.assertEqual(self.event.date, date(2026, 8, 20))
        self.assertEqual(self.event.start_time, time(10, 0))
        self.assertEqual(self.event.capacity, 20)
        self.assertFalse(self.event.approved)

# Test 2: Check if the event can be approved

    def test_event_approval(self):
        # Approve the event
        self.event.approved = True
        self.event.save() # Save the changes to the event

        # Check if the event is approved
        self.assertTrue(self.event.approved)
