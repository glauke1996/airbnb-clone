from django.db import models
from django.utils import timezone
from core import models as core_models

# Create your models here.


class Reservation(core_models.AbstractTimeStampedModel):
    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "pending"),
        (STATUS_CONFIRMED, "confirmed"),
        (STATUS_CANCELED, "canceled"),
    )

    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=12, default="pending")
    guest = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="reservation_room"
    )

    def __str__(self):
        return f"{self.room}-{self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True
    # I have no idea what it is

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True
