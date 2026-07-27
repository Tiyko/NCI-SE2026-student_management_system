from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import EventForm

# Create event page views (Nerijus Kmitas x24170232)
# Only logged-in users can access this page (Nerijus Kmitas x24170232)
@login_required
def create_event(request):

    # Allow only admin or Organiser to create events
    if not request.user.is_superuser:

        # If the user is not an Organiser, access is denied
        if request.user.userprofile.role != "Organizer":
            messages.error(
                request,
                "You are not allowed to create events."
            )

            # Redirect unauthorized users back to the events page
            return redirect("events")

    # Check if the user submitted the form
    if request.method == "POST":

        # Create a form instance using the submitted data
        form = EventForm(request.POST)

        # Check whether all entered data is valid
        if form.is_valid():

            # Create the event object without saving it yet
            event = form.save(commit=False)

            # Automatically assign the logged-in user
            # as the Organiser of the event
            event.organiser = request.user

            # Organiser events needs admin approval before it is visible for students
            event.approved = False

            # Save the event to the database
            event.save()

            # Redirect to the event page after successful creation
            return redirect("events")

    else:

        # If page is opened normally (GET request),
        # create an empty form
        form = EventForm()


    # Display the Create Event page with the form
    return render(
        request,
        "home/create_event.html",
        {
            "form": form
        }
    )