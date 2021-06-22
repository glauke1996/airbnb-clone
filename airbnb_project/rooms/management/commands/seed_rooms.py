import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number", help="this command creates the rooms as much as you want."
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_user = user_models.User.objects.all()  # maybe return dic
        room_types = room_models.RoomType.objects.all()
        # print(room_types)
        # print(all_user)
        seeder.add_entity(
            room_models.Room,
            int(number),
            {
                "guests": lambda x: random.randint(0, 5),
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_user),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(0, 300),
                "beds": lambda x: random.randint(0, 5),
                "bedrooms": lambda x: random.randint(0, 3),
                "bath": lambda x: random.randint(0, 3),
            },
        )
        created_PK = (
            seeder.execute()
        )  # according to seed_documentation, returns list of inserted pks
        created_clean = flatten(list(created_PK.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            room = room_models.Room.objects.get(id=pk)
            for i in range(3, random.randint(10, 17)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file="/room_photos/{random.randint(1,31)}.webp",
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenity.add(a)  # ForManyToMany
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facility.add(f)
            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rule.add(r)
        self.stdout.write(
            self.style.SUCCESS(f"{number} rooms are succesfully created!")
        )
