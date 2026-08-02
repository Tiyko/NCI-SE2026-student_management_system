from datetime import date, time

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from homepage.models import Event

# Aidas Kibas - Unit Tests for Approve Event Feature

# This test case checks the functionality of approving and rejecting events in the system. It sets up a test organiser and a test event, then verifies that the event can be approved and rejected correctly.

class ApproveEventTests(TestCase):
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

# Checking if the event can be approved and rejected correctly.

# Test 1: Check if the event can be approved
    def test_approve_event(self):
        # Approve the event
        self.event.approved = True
        self.event.save()

        # Check if the event is approved
        self.assertTrue(self.event.approved)

# Test 2: Check if the event can be rejected

    def test_reject_event(self):
        # Reject the event
        self.event.approved = False
        self.event.save()

        # Check if the event is rejected
        self.assertFalse(self.event.approved)