from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):
    help = "This command creates amenities. "

    """  def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to say ara ara?"
        ) """

    def handle(self, *args, **options):
        amenities = [
            "Wi-Fi",
            "Washer",
            "Drier",
            "Towel",
            "Massages",
            "Tv",
            "Air conditioner",
            "Shampoo",
            "lotion",
            "cleanser",
            "pillows",
            "blankets",
            "Balcony",
            "Flower box",
            "bin",
            "View Of Sea",
        ]
        for a in amenities:
            room_models.Amenity.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("Amenities created!!"))
