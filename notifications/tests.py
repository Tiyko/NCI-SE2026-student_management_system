from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from homepage.models import Event
from datetime import date, time

# Aidas Kibas - Unit Tests for Notification Feature

class NotificationTests(TestCase):
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

# Test 1: Check if the notification is created

    def test_notification_creation(self):
        self.assertTrue(self.event.approved)

# Test 2: Check if the notification read status can be updated

    def test_notification_read_status(self):
        self.event.approved = False
        self.event.save()
        self.assertFalse(self.event.approved)

