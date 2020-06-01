from django.core.management.base import BaseCommand, CommandError
from app.models import *
from app.tasks import *

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        initiate_due_notifications_for_all_deltas.apply_async()
