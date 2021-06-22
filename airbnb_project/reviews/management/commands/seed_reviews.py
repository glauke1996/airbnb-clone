import random
from django.core.management.base import BaseCommand  # django
from django_seed import Seed  # third party
from reviews import models as reviews_models  # local
from users import models as users_models
from rooms import models as rooms_models


class Command(BaseCommand):
    help = "This command creates fake users "

    def add_arguments(self, parser):
        parser.add_argument("--number", help="How many reviews do you want to create?")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = users_models.User.objects.all()
        rooms = rooms_models.Room.objects.all()
        seeder.add_entity(
            reviews_models.reviews,
            number,
            {
                "accuracy": lambda x: random.randint(0, 6),
                "communication": lambda x: random.randint(0, 6),
                "cleanliness": lambda x: random.randint(0, 6),
                "location": lambda x: random.randint(0, 6),
                "check_in": lambda x: random.randint(0, 6),
                "value": lambda x: random.randint(0, 6),
                "users": lambda x: random.choice(users),
                "rooms": lambda x: random.choice(rooms),
            },
        )

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews created!!"))
