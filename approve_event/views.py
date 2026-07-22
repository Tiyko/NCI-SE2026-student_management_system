from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

from homepage.models import Event

# Create your views here.

@staff_member_required
def approve_events(request):

    pending_events = Event.objects.filter(
        approved=False
    )

    return render(
        request,
        "home/approve_events.html",
        {
            "events": pending_events
        }
    )


@staff_member_required
def approve_event(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id
    )

    event.approved = True
    event.save()

    return redirect('approve_events')


@staff_member_required
def reject_event(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id
    )

    event.delete()

    return redirect('approve_events')