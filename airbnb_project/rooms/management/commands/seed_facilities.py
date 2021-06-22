from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):
    help = "This command creates facilites. "

    """  def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to say ara ara?"
        ) """

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
            "Swimming Pool",
            "Convenient Store",
        ]

        for f in facilities:
            room_models.Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS("Facilities created!!"))
