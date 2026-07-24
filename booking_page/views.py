from urllib import request

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from homepage.models import Event
from .models import Booking


@login_required
def booking_page(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":

        existing_booking = Booking.objects.filter(
            student=request.user,
            event=event
        ).exists()


        if existing_booking:

            messages.warning(
                request,
                "You are already booked for this event."
            )

        else:

            Booking.objects.create(
                student=request.user,
                event=event
            )

            messages.success(
                request,
                "Your booking was successful!"
            )


        return redirect("events")


    return render(
        request,
        "home/booking_page.html",
        {
            "event": event
        }
    )

@login_required
def request_refund(request):
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
            messages.info(
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