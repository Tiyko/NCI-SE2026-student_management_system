from django.shortcuts import render
from homepage.models import Event


def events(request):
    event_list = Event.objects.filter(approved=True)

    return render(
        request,
        "home/events.html",
        {
            "events": event_list,
        },
    )