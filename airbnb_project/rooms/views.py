from django.views.generic import ListView, DetailView, UpdateView, FormView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.http import Http404
from django_countries import countries
from rooms import models as room_model
from rooms import forms as room_form

# from django.http import HttpResponse # django translate the request
# Create your views here.


class HomeView(ListView):

    """Home View Definition"""

    model = room_model.Room
    paginate_by = 12
    context_object_name = "page"
    ordering = "created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()  # get_context_data search in doc
        context["now"] = now
        return context


def room_detail(request, pk):
    try:
        room = room_model.Room.objects.get(pk=pk)
        print(dir(room))
        return render(request, "rooms/detail.html", context={"room": room})
    except room_model.Room.DoesNotExist:
        # return redirect(reverse("core:home"))  # reverse returns url
        raise Http404()


# class ModelNameDetail(DetailView):
#     model = room_model.Room
#     pk_url_kwarg="pk"
# you don't need to raise the http 404~
# to more customize this, look it up on the CCBV


class EditRoomView(UpdateView):
    model = room_model.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "bath",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenity",
        "facility",
        "house_rule",
    )


class CreateRoomView(FormView):
    form_class = room_form.CreateRoomForm
    template_name = "rooms/room_create.html"


# class RoomPhotosView(DetailView):
#     model = room_model.Room
#     template_name = "rooms/room_photos.html"

#     def get(self, queryset=None):  # override
#         room = super().get_object(queryset=queryset)
#         if room.host.pk != self.request.user.pk:
#             raise Http404()
#         return room


def Search(request):
    city = request.GET.get("city", "anywhere")
    room_type = int(request.GET.get("room_type", 0))
    room_types = room_model.RoomType.objects.all()
    country = request.GET.get("country", "KR")
    print(country)
    form = {
        "city": city,
        "s_room_type": room_type,  # from database
        "s_country": country,
    }

    choices = {
        "countries": countries,
        "room_types": room_types,
    }

    return render(
        request,
        template_name="rooms/search.html",
        context={**form, **choices},
    )
