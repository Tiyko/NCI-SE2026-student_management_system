from django.db import models
from django.contrib.auth.models import User

from homepage.models import Event

#   Edited by:
#   Ionut Ciobanu
#


class Notification(models.Model):

	# Notification types shown in the sender form and in the student inbox.
	TYPE_EVENT_UPDATE = "event_update"
	TYPE_REMINDER = "reminder"
	TYPE_ANNOUNCEMENT = "announcement"

	NOTIFICATION_TYPE_CHOICES = [
		(TYPE_EVENT_UPDATE, "Event Update"),
		(TYPE_REMINDER, "Reminder"),
		(TYPE_ANNOUNCEMENT, "Announcement"),
	]

	AUDIENCE_ALL_STUDENTS = "all_students"
	AUDIENCE_EVENT_PARTICIPANTS = "event_participants"

	AUDIENCE_CHOICES = [
		(AUDIENCE_ALL_STUDENTS, "All Students"),
		(AUDIENCE_EVENT_PARTICIPANTS, "Event Participants"),
	]

	sender = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name="sent_notifications",
	)

	notification_type = models.CharField(
		max_length=30,
		choices=NOTIFICATION_TYPE_CHOICES,
	)

	audience_type = models.CharField(
		max_length=30,
		choices=AUDIENCE_CHOICES,
	)

	event = models.ForeignKey(
		Event,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="notifications",
	)

	message = models.TextField()

	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.get_notification_type_display()} ({self.created_at:%Y-%m-%d %H:%M})"


class NotificationRecipient(models.Model):

	# This join table stores one receipt per recipient so read state is per user.
	notification = models.ForeignKey(
		Notification,
		on_delete=models.CASCADE,
		related_name="recipient_links",
	)

	recipient = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name="notification_receipts",
	)

	delivered_at = models.DateTimeField(auto_now_add=True)
	read_at = models.DateTimeField(null=True, blank=True)
	email_sent = models.BooleanField(default=False)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=["notification", "recipient"],
				name="unique_notification_recipient",
			)
		]

	def __str__(self):
		return f"{self.recipient.username} <- {self.notification_id}"

	@property
	def is_read(self):
		# Treat a populated timestamp as the read flag.
		return self.read_at is not None

	def mark_as_read(self):
		# Keep the helper idempotent so repeated clicks are harmless.
		if self.read_at is None:
			from django.utils import timezone

			self.read_at = timezone.now()
			self.save(update_fields=["read_at"])

	def mark_as_unread(self):
		# Clearing the timestamp is enough to switch the receipt back to unread.
		if self.read_at is not None:
			self.read_at = None
			self.save(update_fields=["read_at"])
