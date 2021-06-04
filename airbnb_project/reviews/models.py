from django.db import models
from core import models as core_models

# Create your models here.
class reviews(core_models.AbstractTimeStampedModel):
    """Reviews Model Definition"""

    Review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="review_user"
    )
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="review_room"
    )

    def __str__(self):
        return f"{self.Review} - {self.room}"
