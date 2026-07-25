from django.urls import path

from . import views

#   Edited by:
#   Ionut Ciobanu
#


urlpatterns = [
	# Notification inbox and admin send view share the same entry point.
    path("", views.notifications_page, name="notifications"),
	# Student-side toggle for one receipt row.
    path("<int:recipient_id>/toggle-read/", views.toggle_notification_read, name="notification_toggle_read"),
	# Bulk action for clearing unread badges in the dropdown and inbox.
    path("mark-all-read/", views.mark_all_notifications_read, name="notification_mark_all_read"),
	# Admin-only delete action for the manage notifications.
	path("<int:notification_id>/delete/", views.delete_notification, name="notification_delete"),
]
