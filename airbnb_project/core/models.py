from django.db import models

# Create your models here.
class AbstractTimeStampedModel(models.Model):

    """TimeStampedModel"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(
        auto_now=True
    )  # one of the cool function that Django have

    class Meta:
        abstract = True
