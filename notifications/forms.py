from django import forms

from homepage.models import Event

from .models import Notification


class NotificationForm(forms.ModelForm):

    class Meta:
        model = Notification

        fields = [
            "notification_type",
            "audience_type",
            "event",
            "message",
        ]

        widgets = {
            "notification_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "audience_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "event": forms.Select(
                attrs={"class": "form-select"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Write your notification message",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["event"].queryset = Event.objects.filter(approved=True).order_by("date", "start_time")
        self.fields["event"].required = False
        self.fields["event"].empty_label = "Select an event"

    def clean(self):
        cleaned_data = super().clean()

        audience_type = cleaned_data.get("audience_type")
        event = cleaned_data.get("event")
        message = cleaned_data.get("message")

        if audience_type == Notification.AUDIENCE_EVENT_PARTICIPANTS and not event:
            self.add_error("event", "Please select an event for event participants.")

        if message and not message.strip():
            self.add_error("message", "Message cannot be empty.")

        return cleaned_data
