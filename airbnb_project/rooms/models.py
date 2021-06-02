from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models

# Create your models here.
class Photo(core_models.AbstractTimeStampedModel):

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey("Room", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class AbstractItem(core_models.AbstractTimeStampedModel):
    """Item"""

    name = models.CharField(max_length=80)

    class meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """RoomType_Model_Definition"""

    class meta:
        verbose_name_plural = "Room Type"


class Amenity(AbstractItem):
    """Amenity_Model_Definition"""

    class meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """Facility_Model_Definition"""

    class meta:
        verbose_name_plural = "Facilities"


class HouseRULE(AbstractItem):
    """HouseRule_Moel_Definition"""

    class meta:
        verbose_name_plural = "House Rule"


class Room(core_models.AbstractTimeStampedModel):
    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    bath = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room_type = models.ForeignKey("RoomType", on_delete=models.SET_NULL, null=True)
    amenity = models.ManyToManyField("Amenity")
    facility = models.ManyToManyField("Facility")
    house_rule = models.ManyToManyField("HouseRULE")

    def __str__(self):
        return self.name
