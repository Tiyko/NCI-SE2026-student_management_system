from django.db import models
from django.contrib.auth.models import User
from homepage.models import Event

# Booking page models (Nerijus Kmitas x24170232)
# Create the Booking database model
class Booking(models.Model):

    # Connect each booking to a student/user.
    # ForeignKey creates a many-to-one relationship
    # One student can have many bookings.
    student = models.ForeignKey(
        User,
        # If user is deleted, all bookings related to that user, will be also deleted
        on_delete=models.CASCADE,
        # Allows accessing all booking made by user
        # user.booking.all()
        related_name="bookings"
    )

    # Connect each booking to an event
    # One event can have many bookings
    event = models.ForeignKey(
        Event,
        # If an event is deleted, than all related bookings will also be deleted
        on_delete=models.CASCADE,
        # Allows accessing all bookings for an event
        # event.bookings.all()
        related_name="bookings"
    )

    # It will automatically stores the date and time when booking is created
    # value is set only once when the record has been created
    booked_at = models.DateTimeField(auto_now_add=True)

    # Additional rules and settings for this model
    class Meta:
        # Prevent the same student book the event more than once
        constraints = [
            models.UniqueConstraint(
                # Combination of student and the event mus be always unique
                fields=["student", "event"],
                # Name that is given to this database constraint
                name="unique_booking"
            )
        ]

    # Controls how booking object is displayed in Django admin panel and shell
    def __str__(self):
        # That will display booking information as:
        # "username - event title"
        return f"{self.student.username} - {self.event.title}"