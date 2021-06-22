from django.core.management.base import BaseCommand


class Command(BaseCommand):
    print("hello")
    help = "This command say to me ara ara. "

    def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to say ara ara?"
        )

    def handle(self, *args, **options):
        print(options)
        times = options.get("times")
        for i in range(int(times)):
            print("i love you")
