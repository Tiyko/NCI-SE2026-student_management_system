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

    approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Organizer', 'Organizer'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="Student"
    )


    def __str__(self):
        return f"{self.user.username} - {self.role}"