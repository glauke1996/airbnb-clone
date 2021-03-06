from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from rooms import models as room_model
from . import models

# Create your views here.


def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_model.Room.objects.get(pk=room_pk)
    if room != None and action != None:
        the_list, _ = models.List.objects.get_or_create(
            user=request.user, name="My Favorites"
        )
        if action == "add":
            the_list.rooms.add(room)
        elif action == "remove":
            the_list.rooms.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(TemplateView):
    template_name = "lists/list_detail.html"
