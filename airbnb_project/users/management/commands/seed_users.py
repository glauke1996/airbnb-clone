from django.core.management.base import BaseCommand  # django
from django_seed import Seed  # third party
from users import models as user_models  # local


class Command(BaseCommand):
    help = "This command creates fake users "

    def add_arguments(self, parser):
        parser.add_argument("--number", help="How many users do you want to create?")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            user_models.User, int(number), {"is_staff": False, "is_superuser": False}
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} Users created!!"))
