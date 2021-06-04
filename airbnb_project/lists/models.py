from django.db import models
from core import models as core_models

# Create your models here.


class List(core_models.AbstractTimeStampedModel):
    name = models.CharField(max_length=80)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="List_user"
    )
    rooms = models.ManyToManyField("rooms.Room", blank=True, related_name="List_rooms")

    def __str__(self):
        return self.name
