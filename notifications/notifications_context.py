from .models import NotificationRecipient

#   Edited by:
#   Ionut Ciobanu
#


def notification_dropdown(request):
	# Anonymous users do not need notification data in the navigation.
	if not request.user.is_authenticated:
		return {}

	# Reuse the recipient join table so the dropdown can show read/unread state.
	notification_receipts = (
		NotificationRecipient.objects.filter(recipient=request.user)
		.select_related("notification", "notification__sender", "notification__event")
		.order_by("-notification__created_at")
	)

	return {
		"notification_dropdown_items": notification_receipts[:5],
		"notification_unread_count": notification_receipts.filter(read_at__isnull=True).count(),
	}