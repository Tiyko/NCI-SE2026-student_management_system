from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):

    SPORT_CHOICES = [
        ('Football', 'Football'),
        ('Basketball', 'Basketball'),
        ('Tennis', 'Tennis'),
        ('Volleyball', 'Volleyball'),
        ('Other', 'Other'),
    ]

    organiser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="events"
    )

    title = models.CharField(max_length=200)

    sport_type = models.CharField(
        max_length=50,
        choices=SPORT_CHOICES
    )

    location = models.CharField(max_length=200)

    date = models.DateField()

    start_time = models.TimeField()

    capacity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title