from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):  # inheritence

    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )
    LANGUAGE_ENG = "en"
    LANGUAGE_KOR = "kr"

    LANGUAGE_CHOICES = (
        (
            LANGUAGE_ENG,
            "english",
        ),
        (LANGUAGE_KOR, "korean"),
    )
    # left one go to database and another one shows on the form
    CURRENCY_USD = "usd"
    CURRENCY_krw = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "usd"), (CURRENCY_krw, "krw"))

    avatar = models.ImageField(blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True)
    superhost = models.BooleanField(default=False)
