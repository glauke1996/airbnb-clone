from django import forms
from django_countries.fields import CountryField
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

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = room_model.Photo
        fields = ("caption", "file")

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = room_model.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False,
        empty_label="Any kind",
        queryset=room_model.RoomType.objects.all(),
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=room_model.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=room_model.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
