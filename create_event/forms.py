from django import forms
from homepage.models import Event

# Create event page form (Nerijus Kmitas x24170232)
# Event creation form
class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            'title',
            'sport_type',
            'location',
            'date',
            'start_time',
            'capacity',
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'start_time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
        }