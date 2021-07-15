from django.core.checks import messages
from django.shortcuts import render
from django.views.generic import ListView
import datetime
from rooms import models as room_model
from django.shortcuts import redirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import View
from . import models
from reviews import forms
import reservations

# Create your views here.
class CreateError(Exception):
    pass


def CreateReservationView(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_model.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (room_model.Room.DoesNotExist, CreateError):
        return redirect(reverse("core:home"))
    except (models.BookedDay.DoesNotExist):
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        reservation.save()
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        try:
            pk = kwargs.get("pk")
            reservation = models.Reservation.objects.get(pk=pk)
        except (models.Reservation.DoesNotExist):
            raise Http404()
        if (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        form = forms.CreateReviewForm()
        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation, "form": form},
        )


def EditReservationView(request, pk, verb):
    try:
        reservation = models.Reservation.objects.get(pk=pk)
        room = reservation.room
    except (models.Reservation.DoesNotExist):
        raise Http404()
    # if reservation.guest != request.user and reservation.room.host != request.user:
    #     raise Http404()

    if verb == "confirm":
        reservation.status = reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = reservation.STATUS_CANCELED
        reservation.delete()
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
    reservation.save()
    redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class MyReservationView(ListView):
    model = models.Reservation
    paginate_by = 10
    ordering = "created"
