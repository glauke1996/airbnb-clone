import random
from django.core.management.base import BaseCommand  # django
from datetime import datetime, timedelta
from django_seed import Seed  # third party
from reservations import models as reservations_models  # local
from users import models as users_models
from rooms import models as rooms_models


class Command(BaseCommand):
    help = "This command creates fake reservations "

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", help="How many reservations do you want to create?"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = users_models.User.objects.all()
        rooms = rooms_models.Room.objects.all()
        seeder.add_entity = (
            reservations_models.Reservation,
            int(number),
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25))
                # timedelta
            },
        )

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reservations created!!"))
