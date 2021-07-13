from django.db import models
from django.utils import timezone
import datetime
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

    def save(self, *args, **kwargs):
        if self.pk == None:
            start = self.check_in  # datetime eg)00-00-00
            end = self.check_out
            difference = end - start  # O day
            existing_booked_day = BookedDay.objects.filter(
                day__range=(start, end)
            ).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)  # Maybe pk is given here
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)


class BookedDay(core_models.AbstractTimeStampedModel):
    day = models.DateField()
    reservation = models.ForeignKey(
        "Reservation", related_name="booked_day", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"
