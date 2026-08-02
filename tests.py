from datetime import date, timedelta, time

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from booking_page.models import Booking
from homepage.models import Event
from homepage.models import UserProfile
from notifications.models import Notification
from notifications.models import NotificationRecipient

# Edited by:
#  Ionut Ciobanu
# 

class IntegrationTests(TestCase):
	def _create_event(self, **overrides):
		organiser = overrides.pop("organiser", None) or User.objects.create_user(
			username="organiser",
			email="organiser@example.com",
			password="StrongPass123!",
		)

		defaults = {
			"organiser": organiser,
			"title": "Campus Football Night",
			"sport_type": "Football",
			"location": "Main Hall",
			"date": date.today() + timedelta(days=1),
			"start_time": time(18, 0),
			"capacity": 10,
			"approved": True,
		}
		defaults.update(overrides)
		return Event.objects.create(**defaults)

	def _signup_payload(self, **overrides):
		payload = {
			"first_name": "Test",
			"last_name": "Student",
			"email": "student@example.com",
			"username": "student1",
			"password1": "StrongPass123!",
			"password2": "StrongPass123!",
		}
		payload.update(overrides)
		return payload

	def test_it01_authentication_database_registration_creates_user(self):
		response = self.client.post(
			reverse("account_signup"),
			data=self._signup_payload(),
		)

		self.assertEqual(response.status_code, 302)
		self.assertTrue(User.objects.filter(email="student@example.com").exists())

		created_user = User.objects.get(email="student@example.com")
		self.assertEqual(created_user.first_name, "Test")
		self.assertEqual(created_user.last_name, "Student")
		self.assertIn("_auth_user_id", self.client.session)

	def test_it02_authentication_database_duplicate_email_is_rejected(self):
		User.objects.create_user(
			username="existinguser",
			email="existing@example.com",
			password="StrongPass123!",
		)

		response = self.client.post(
			reverse("account_signup"),
			data=self._signup_payload(
				email="existing@example.com",
				username="differentuser",
			),
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(User.objects.filter(email="existing@example.com").count(), 1)
		self.assertContains(response, "A user is already registered with this email address.")

	def test_it03_authentication_event_module_requires_valid_session(self):
		event = self._create_event()

		response = self.client.get(reverse("events"))
		self.assertRedirects(
			response,
			f"{reverse('account_login')}?next={reverse('events')}",
		)

		user = User.objects.create_user(
			username="eventuser",
			email="eventuser@example.com",
			password="StrongPass123!",
		)
		self.client.force_login(user)

		response = self.client.get(reverse("events"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, event.title)

	def test_it04_event_module_database_handles_no_events(self):
		user = User.objects.create_user(
			username="noeventsuser",
			email="noevents@example.com",
			password="StrongPass123!",
		)
		self.client.force_login(user)

		response = self.client.get(reverse("events"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No events available.")

	def test_it05_event_module_booking_module_passes_event_details(self):
		user = User.objects.create_user(
			username="bookingviewer",
			email="bookingviewer@example.com",
			password="StrongPass123!",
		)
		self.client.force_login(user)

		event = self._create_event(
			title="Basketball Finals",
			sport_type="Basketball",
			location="Sports Arena",
		)

		response = self.client.get(reverse("booking_page", args=[event.id]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Basketball Finals")
		self.assertContains(response, "Basketball")
		self.assertContains(response, "Sports Arena")

	def test_it06_booking_module_database_successful_booking(self):
		user = User.objects.create_user(
			username="booker",
			email="booker@example.com",
			password="StrongPass123!",
		)
		self.client.force_login(user)

		event = self._create_event(capacity=2)

		response = self.client.post(
			reverse("booking_page", args=[event.id]),
			data={},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.assertTrue(Booking.objects.filter(student=user, event=event).exists())
		self.assertContains(response, "Your booking was successful!")

		event.refresh_from_db()
		available_places = event.capacity - event.bookings.count()
		self.assertEqual(available_places, 1)

	def test_it07_booking_module_event_module_sold_out_handling(self):
		user = User.objects.create_user(
			username="soldoutuser",
			email="soldout@example.com",
			password="StrongPass123!",
		)
		self.client.force_login(user)

		event = self._create_event(capacity=0)

		response = self.client.post(
			reverse("booking_page", args=[event.id]),
			data={},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.assertFalse(Booking.objects.filter(student=user, event=event).exists())
		self.assertContains(response, "Sorry, this event is sold out.")

	def test_it08_authentication_booking_module_blocks_unauthenticated_booking(self):
		event = self._create_event()

		get_response = self.client.get(reverse("booking_page", args=[event.id]))
		self.assertRedirects(
			get_response,
			f"{reverse('account_login')}?next={reverse('booking_page', args=[event.id])}",
		)

		post_response = self.client.post(reverse("booking_page", args=[event.id]), data={})
		self.assertRedirects(
			post_response,
			f"{reverse('account_login')}?next={reverse('booking_page', args=[event.id])}",
		)

	def test_it09_notifications_module_announcements_are_delivered_to_students(self):
		admin_user = User.objects.create_superuser(
			username="adminuser",
			email="admin@example.com",
			password="StrongPass123!",
		)
		student_one = User.objects.create_user(
			username="student_one",
			email="student_one@example.com",
			password="StrongPass123!",
		)
		student_two = User.objects.create_user(
			username="student_two",
			email="student_two@example.com",
			password="StrongPass123!",
		)

		UserProfile.objects.create(user=student_one, role="Student")
		UserProfile.objects.create(user=student_two, role="Student")

		self.client.force_login(admin_user)
		response = self.client.post(
			reverse("notifications"),
			data={
				"notification_type": Notification.TYPE_ANNOUNCEMENT,
				"audience_type": Notification.AUDIENCE_ALL_STUDENTS,
				"event": "",
				"message": "Campus closes early tomorrow.",
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Notification sent to 2 recipient(s).")

		notification = Notification.objects.get(message="Campus closes early tomorrow.")
		recipients = NotificationRecipient.objects.filter(notification=notification)
		self.assertEqual(recipients.count(), 2)
		self.assertTrue(recipients.filter(recipient=student_one).exists())
		self.assertTrue(recipients.filter(recipient=student_two).exists())

		self.client.force_login(student_one)
		student_inbox = self.client.get(reverse("notifications"))
		self.assertEqual(student_inbox.status_code, 200)
		self.assertContains(student_inbox, "My Notifications")
		self.assertContains(student_inbox, "Campus closes early tomorrow.")

	def test_it10_notifications_module_event_updates_reach_only_event_participants(self):
		admin_user = User.objects.create_superuser(
			username="adminnotify",
			email="adminnotify@example.com",
			password="StrongPass123!",
		)
		participant = User.objects.create_user(
			username="participant",
			email="participant@example.com",
			password="StrongPass123!",
		)
		non_participant = User.objects.create_user(
			username="nonparticipant",
			email="nonparticipant@example.com",
			password="StrongPass123!",
		)

		event = self._create_event(title="Tennis Session", sport_type="Tennis")
		Booking.objects.create(student=participant, event=event)

		self.client.force_login(admin_user)
		response = self.client.post(
			reverse("notifications"),
			data={
				"notification_type": Notification.TYPE_EVENT_UPDATE,
				"audience_type": Notification.AUDIENCE_EVENT_PARTICIPANTS,
				"event": event.id,
				"message": "Tennis Session starts 30 minutes earlier.",
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Notification sent to 1 recipient(s).")

		notification = Notification.objects.get(message="Tennis Session starts 30 minutes earlier.")
		recipients = NotificationRecipient.objects.filter(notification=notification)
		self.assertEqual(recipients.count(), 1)
		self.assertTrue(recipients.filter(recipient=participant).exists())
		self.assertFalse(recipients.filter(recipient=non_participant).exists())

		self.client.force_login(participant)
		participant_inbox = self.client.get(reverse("notifications"))
		self.assertEqual(participant_inbox.status_code, 200)
		self.assertContains(participant_inbox, "Tennis Session starts 30 minutes earlier.")

		self.client.force_login(non_participant)
		other_inbox = self.client.get(reverse("notifications"))
		self.assertEqual(other_inbox.status_code, 200)
		self.assertNotContains(other_inbox, "Tennis Session starts 30 minutes earlier.")
