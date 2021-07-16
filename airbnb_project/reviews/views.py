from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms
from rooms import models as room_model

# Create your views here.


def CreateReviewView(request, room):
    if request.method == "POST":
        try:
            form = forms.CreateReviewForm(request.POST)
            room = room_model.Room.objects.get(pk=room)
        except room.DoesNotExist:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
