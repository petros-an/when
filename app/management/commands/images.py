from django.core.management.base import BaseCommand, CommandError
from app.scripts import images
class Command(BaseCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        images.run()
