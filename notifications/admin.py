from django.contrib import admin

from .models import Notification, NotificationRecipient

#   Edited by:
#   Ionut Ciobanu
#


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
	# Keep the sender-side list focused on the fields admins actually filter by.
	list_display = (
		"id",
		"notification_type",
		"audience_type",
		"event",
		"sender",
		"created_at",
	)
	list_filter = ("notification_type", "audience_type", "created_at")
	search_fields = ("message", "sender__username", "event__title")


@admin.register(NotificationRecipient)
class NotificationRecipientAdmin(admin.ModelAdmin):
	# Expose read state in the admin so support can inspect delivery progress quickly.
	list_display = ("notification", "recipient", "delivered_at", "read_at", "email_sent")
	list_filter = ("email_sent", "read_at", "delivered_at")
	search_fields = ("recipient__username", "recipient__email")
