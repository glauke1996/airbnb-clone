from django import forms
from . import models as room_model


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = room_model.Room
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
