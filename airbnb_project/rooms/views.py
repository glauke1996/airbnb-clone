from django.forms.forms import Form
from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, FormView, View
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django_countries import countries
from rooms import forms, models as room_model
from reservations import models as res_model
from rooms import forms as room_form
from users import mixins
from users.mixins import LoggedInOnlyView


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
        reservations = res_model.Reservation.objects.filter(room=room)
        for reservation in reservations:
            if reservation.is_finished():
                reservation.delete()
        return render(request, "rooms/detail.html", context={"room": room})
    except room_model.Room.DoesNotExist:
        # return redirect(reverse("core:home"))  # reverse returns url
        raise Http404()


# class ModelNameDetail(DetailView):
#     model = room_model.Room
#     pk_url_kwarg="pk"
# you don't need to raise the http 404~
# to more customize this, look it up on the CCBV


class EditRoomView(LoggedInOnlyView, UpdateView):
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

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class UploadRoomView(FormView, mixins.LoggedInOnlyView):
    form_class = room_form.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))


class RoomPhotosView(DetailView):
    model = room_model.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):  # override
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rooms = room_model.Room.objects.all()
        context["rooms"] = rooms
        return context


# class SearchView(View):
#     def get(self, request):

#         country = request.GET.get("country")

#         if country:

#             form = forms.SearchForm(request.GET)

#             if form.is_valid():

#                 city = form.cleaned_data.get("city")
#                 country = form.cleaned_data.get("country")
#                 room_type = form.cleaned_data.get("room_type")
#                 price = form.cleaned_data.get("price")
#                 guests = form.cleaned_data.get("guests")
#                 bedrooms = form.cleaned_data.get("bedrooms")
#                 beds = form.cleaned_data.get("beds")
#                 baths = form.cleaned_data.get("baths")
#                 instant_book = form.cleaned_data.get("instant_book")
#                 superhost = form.cleaned_data.get("superhost")
#                 amenities = form.cleaned_data.get("amenities")
#                 facilities = form.cleaned_data.get("facilities")

#                 filter_args = {}

#                 if city != "Anywhere":
#                     filter_args["city__startswith"] = city

#                 filter_args["country"] = country

#                 if room_type is not None:
#                     filter_args["room_type"] = room_type

#                 if price is not None:
#                     filter_args["price__lte"] = price

#                 if guests is not None:
#                     filter_args["guests__gte"] = guests

#                 if bedrooms is not None:
#                     filter_args["bedrooms__gte"] = bedrooms

#                 if beds is not None:
#                     filter_args["beds__gte"] = beds

#                 if baths is not None:
#                     filter_args["baths__gte"] = baths

#                 if instant_book is True:
#                     filter_args["instant_book"] = True

#                 if superhost is True:
#                     filter_args["host__superhost"] = True

#                 for amenity in amenities:
#                     filter_args["amenities"] = amenity

#                 for facility in facilities:
#                     filter_args["facilities"] = facility

#                 rooms = room_model.Room.objects.filter(**filter_args)

#         else:

#             form = forms.SearchForm()

#         return render(request, "rooms/search.html", {"form": form, "rooms": rooms})


def Search(request):
    city = request.GET.get("city", "anywhere")
    room_type = int(request.GET.get("room_type", 0))
    room_types = room_model.RoomType.objects.all()
    country = request.GET.get("country", "KR")
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    beds = int(request.GET.get("beds", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    bath = int(request.GET.get("bath", 0))

    amenities = room_model.Amenity.objects.all()
    facilities = room_model.Facility.objects.all()
    form = {
        "city": city,
        "s_room_type": room_type,  # from database
        "s_country": country,
        "price": price,
        "guests": guests,
        "beds": beds,
        "bedrooms": bedrooms,
        "bath": bath,
    }
    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }
    filter_args = {}
    if city != "anywhere":
        filter_args["city__startswith"] = city
    filter_args["country"] = country
    if room_type != 0:
        filter_args["room_type__pk"] = room_type
    if price != 0:
        filter_args["price__lte"] = price  # refer to lookup session on documentation
    if guests != 0:
        filter_args["guests__gte"] = guests
    if beds != 0:
        filter_args["beds__gte"] = beds
    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms
    if bath != 0:
        filter_args["bath__gte"] = bath
    rooms = room_model.Room.objects.filter(**filter_args)
    return render(
        request,
        template_name="rooms/search.html",
        context={**form, **choices, "rooms": rooms},
    )


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = room_model.Room.objects.get(pk=room_pk)
        if user.pk != room.host.pk:
            messages.error(request, "can't delete that photo")
        else:
            photo = room_model.Photo.objects.get(pk=photo_pk)
            photo.delete()
            messages.success(request, "Photo is successfully deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))

    except room_model.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(mixins.LoggedInOnlyView, UpdateView):
    model = room_model.Photo
    template_name = "rooms/photo_edit.html"
    fields = ("caption",)
    pk_url_kwarg = "photo_pk"
    success_message = "Photo_updated"

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(mixins.LoggedInOnlyView, FormView, SuccessMessageMixin):
    model = room_model.Photo
    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))
