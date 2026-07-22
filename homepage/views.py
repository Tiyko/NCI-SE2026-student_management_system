from django.shortcuts import render
from .models import Event


def index(request):
    events = Event.objects.all().order_by("date", "start_time")

    return render(
        request,
        "home/index.html",
        {
            "events": events,
        },
    )