import random
from django.core.management.base import BaseCommand  # django
from django.contrib.admin.utils import flatten
from django_seed import Seed  # third party
from lists import models as lists_models  # local
from users import models as users_models
from rooms import models as rooms_models


class Command(BaseCommand):
    help = "This command creates fake lists "

    def add_arguments(self, parser):
        parser.add_argument("--number", help="How many lists do you want to create?")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = users_models.User.objects.all()
        rooms = rooms_models.Room.objects.all()
        seeder.add_entity = (lists_models.List, int(number), {})

        created = seeder.execute()
        created_clean = flatten(list(created_clean.values()))
        for pk in created_clean:
            list_model = lists_models.List.objects.get(pk=id)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} lists created!!"))
