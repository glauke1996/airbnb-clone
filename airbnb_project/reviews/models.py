from django.db import models
from django.forms.fields import NullBooleanField
from core import models as core_models

# Create your models here.
class reviews(core_models.AbstractTimeStampedModel):
    """Reviews Model Definition"""

    NumberChoices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    Review = models.TextField()
    accuracy = models.IntegerField(choices=NumberChoices)
    communication = models.IntegerField(choices=NumberChoices)
    cleanliness = models.IntegerField(choices=NumberChoices)
    location = models.IntegerField(choices=NumberChoices)
    check_in = models.IntegerField(choices=NumberChoices)
    value = models.IntegerField(choices=NumberChoices)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews"
    )
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="reviews"
    )

    def __str__(self):
        return f"{self.Review} - {self.room}"

    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    class Meta:
        ordering = ("-created",)
