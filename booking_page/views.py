from urllib import request

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime

from homepage.models import Event
from .models import Booking

# Booking page (Nerijus Kmitas x24170232)
# Only allow logged-in users to access the booking page
@login_required
def booking_page(request, event_id):

    # Find the event from database using the ID from the URL.
    # If the event does not exist, return error 404 page.
    event = get_object_or_404(Event, id=event_id)

    # Checks if the user submitted the booking form
    if request.method == "POST":

        # Checks if the user already has a booking for this specific event
        existing_booking = Booking.objects.filter(
            student=request.user,
            event=event
        ).exists()


        # If booking is already existing this will prevent duplicate
        if existing_booking:

            # It will display message for the user
            messages.warning(
                request,
                "You are already booked for this event."
            )

        else:
            # Creates a new booking record in the database that will be linked
            # with logged-in user with the selected event
            Booking.objects.create(
                student=request.user,
                event=event
            )

            # Displays success message after booking is created
            messages.success(
                request,
                "Your booking was successful!"
            )

        # After booking processed will return user to the events page
        return redirect("events")

    # If user only opens the page (GET request),
    # displays the booking page with the selected event details
    return render(
        request,
        "home/booking_page.html",
        {
            "event": event
        }
    )

#Aidas Kibas - Refund request page

def request_refund(request):
    bookings = []

    if request.user.is_authenticated:
        bookings = Booking.objects.filter(student=request.user).select_related('event').order_by('-booked_at')

    for booking in bookings:
        event_datetime = datetime.combine(
            booking.event.date,
            booking.event.start_time
        )

        # Make the datetime timezone-aware
        event_datetime = timezone.make_aware(event_datetime)

        booking.is_past = event_datetime < timezone.now()

    return render(request, "home/request_page.html", {
        "bookings": bookings,
    })

def remove_booking(request, booking_id):
    if request.user.is_authenticated:
        try:
            booking = Booking.objects.get(id=booking_id, student=request.user)
            booking.delete()
            messages.success(request, "Booking removed successfully.")
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found.")

    return request_refund(request) 

@login_required
def cancel_booking(request, booking_id):
    bookings = Booking.objects.filter(student=request.user)

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        confirm_refund = request.POST.get("confirm_refund")

        booking = Booking.objects.filter(student=request.user, id=booking_id).first()

        if confirm_refund and booking:
            booking.delete()
            bookings = Booking.objects.filter(student=request.user)
            messages.success(request, "Your refund has been processed.")
        elif booking:
            messages.warning(
                request,
                f"Are you sure you would like to refund this event: {booking.event.title}?"
            )
            return render(
                request,
                "home/request_page.html",
                {
                    "bookings": bookings,
                    "pending_booking": booking,
                }
            )
        else:
            messages.warning(request, "This event does not exist in your booked events.")

    return render(
        request,
        "home/request_page.html",
        {
            "bookings": bookings,
            "pending_booking": None,
        }
    )