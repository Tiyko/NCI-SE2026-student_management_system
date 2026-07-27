from django.shortcuts import render
from homepage.models import Event

# Events page (Nerijus Kmitas x24170232)
def events(request):
    event_list = Event.objects.filter(approved=True)

    # Calculate available places for each event
    for event in event_list:
        event.available_places = event.capacity - event.bookings.count()

    return render(
        request,
        "home/events.html",
        {
            "events": event_list,
        },
    )