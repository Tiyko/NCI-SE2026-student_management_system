from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import NotificationForm
from .models import Notification, NotificationRecipient

#   Edited by:
#   Ionut Ciobanu
#


def _get_redirect_target(request):
	# Send the user back to the page they were already viewing when possible.
	return request.POST.get("next") or request.META.get("HTTP_REFERER") or "notifications"


def _student_notifications_queryset(user):
	# Keep the inbox ordered by the notification creation time instead of the receipt row.
	return (
		NotificationRecipient.objects.filter(recipient=user)
		.select_related("notification", "notification__sender", "notification__event")
		.order_by("-notification__created_at")
	)


def _notification_recipients(audience_type, event):
	# Resolve the recipient set once so create and update share the same delivery rules.
	if audience_type == Notification.AUDIENCE_ALL_STUDENTS:
		return (
			User.objects.filter(userprofile__role="Student")
			.distinct()
			.order_by("id")
		)

	return (
		User.objects.filter(bookings__event=event)
		.distinct()
		.order_by("id")
	)


def _deliver_notification(notification, recipients_list):
	# Rebuild receipt rows so edits always reflect the latest audience selection.
	notification.recipient_links.all().delete()

	recipient_links = [
		NotificationRecipient(
			notification=notification,
			recipient=recipient,
		)
		for recipient in recipients_list
	]
	NotificationRecipient.objects.bulk_create(recipient_links)

	for recipient in recipients_list:
		# Skip email delivery when the user has no address on file.
		if not recipient.email:
			continue

		email_subject = f"{notification.get_notification_type_display()}"
		if notification.event:
			email_subject = f"{email_subject}: {notification.event.title}"

		email_sent = send_mail(
			subject=email_subject,
			message=notification.message,
			from_email=None,
			recipient_list=[recipient.email],
			fail_silently=True,
		)

		if email_sent:
			NotificationRecipient.objects.filter(
				notification=notification,
				recipient=recipient,
			).update(email_sent=True)


@login_required
def notifications_page(request):
	# Superusers keep the admin send form; students get their own inbox view.
	if not request.user.is_superuser:
		notification_receipts = _student_notifications_queryset(request.user)
		return render(
			request,
			"home/student_notifications.html",
			{
				"notification_receipts": notification_receipts,
				"unread_count": notification_receipts.filter(read_at__isnull=True).count(),
			},
		)

	selected_type = request.GET.get("type")
	selected_notification_id = request.GET.get("edit")
	notification_type_values = {
		choice[0] for choice in Notification.NOTIFICATION_TYPE_CHOICES
	}

	initial_data = {}
	editing_notification = None
	if selected_type in notification_type_values:
		initial_data["notification_type"] = selected_type
	if selected_notification_id:
		# Pull an existing notification back into the form for a one-click edit flow.
		drafting_notification = get_object_or_404(Notification, pk=selected_notification_id)
		initial_data = {
			"notification_type": drafting_notification.notification_type,
			"audience_type": drafting_notification.audience_type,
			"event": drafting_notification.event,
			"message": drafting_notification.message,
		}
		editing_notification = drafting_notification

	if request.method == "POST":
		# Build and deliver notifications only when the admin submits the send form.
		notification_id = request.POST.get("notification_id")
		notification_instance = None
		if notification_id:
			# Editing uses the same form, but we bind it to the existing database row.
			notification_instance = get_object_or_404(Notification, pk=notification_id)
		form = NotificationForm(request.POST, instance=notification_instance)

		if form.is_valid():
			audience_type = form.cleaned_data["audience_type"]
			event = form.cleaned_data.get("event")
			recipients = _notification_recipients(audience_type, event)

			recipients_list = list(recipients)
			if not recipients_list:
				form.add_error(None, "No recipients found for the selected audience.")
			else:
				with transaction.atomic():
					# Save the notification first so the recipient rows can reference it.
					notification = form.save(commit=False)
					notification.sender = request.user
					notification.save()
					_deliver_notification(notification, recipients_list)

				messages.success(
					request,
					(
						f"Notification updated for {len(recipients_list)} recipient(s)."
						if notification_instance
						else f"Notification sent to {len(recipients_list)} recipient(s)."
					),
				)
				return redirect("notifications")
	else:
		form = NotificationForm(instance=editing_notification, initial=initial_data)

	recent_notifications = (
		Notification.objects.select_related("event")
		.prefetch_related("recipient_links")
		.order_by("-created_at")[:10]
	)

	return render(
		request,
		"home/notifications.html",
		{
			"form": form,
			"recent_notifications": recent_notifications,
			"editing_notification": editing_notification,
		},
	)


@login_required
@require_POST
def toggle_notification_read(request, recipient_id):
	# Toggle a single notification receipt belonging to the logged-in user.
	recipient = get_object_or_404(
		NotificationRecipient,
		pk=recipient_id,
		recipient=request.user,
	)

	if recipient.is_read:
		recipient.read_at = None
	else:
		recipient.read_at = timezone.now()

	recipient.save(update_fields=["read_at"])
	return redirect(_get_redirect_target(request))


@login_required
@require_POST
def mark_all_notifications_read(request):
	# Bulk-update unread receipts so the dropdown and inbox stay in sync.
	NotificationRecipient.objects.filter(
		recipient=request.user,
		read_at__isnull=True,
	).update(read_at=timezone.now())
	return redirect(_get_redirect_target(request))


@login_required
@require_POST
def delete_notification(request, notification_id):
	# Admin deletes should remove the notification and every recipient receipt row.
	if not request.user.is_superuser:
		messages.error(request, "Only admins can delete notifications.")
		return redirect("home")

	notification = get_object_or_404(Notification, pk=notification_id)
	notification.delete()
	messages.success(request, "Notification deleted.")
	return redirect(_get_redirect_target(request))
