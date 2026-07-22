from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import EventForm


@login_required
def create_event(request):

    # Allow only admin or organiser
    if not request.user.is_superuser:

        if request.user.userprofile.role != "Organizer":
            messages.error(
                request,
                "You are not allowed to create events."
            )

            return redirect("events")


    if request.method == "POST":

        form = EventForm(request.POST)

        if form.is_valid():

            event = form.save(commit=False)

            event.organiser = request.user

            # Organiser events need admin approval
            event.approved = False

            event.save()

            return redirect("events")

    else:

        form = EventForm()


    return render(
        request,
        "home/create_event.html",
        {
            "form": form
        }
    )