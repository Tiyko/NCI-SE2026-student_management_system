from django.db import models
from django.contrib.auth.models import User
from homepage.models import Event

# Create your models here.
class Booking(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "event"],
                name="unique_booking"
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.event.title}"