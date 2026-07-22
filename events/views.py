from django.shortcuts import render
from homepage.models import Event


def events(request):
    event_list = Event.objects.all()

    return render(
        request,
        "home/events.html",
        {
            "events": event_list,
        },
    )