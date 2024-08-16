from django.core.management.base import BaseCommand
from base.models import NewEvent
from django.db.models import Count

class Command(BaseCommand):
    help = 'Identify and handle duplicate destination values'

    def handle(self, *args, **kwargs):
        # Identify duplicate destinations
        duplicates = (
            NewEvent.objects.values('destination')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        for item in duplicates:
            destination = item['destination']
            print(f"Handling duplicates for destination: {destination}")

            # Get the duplicate records
            events = NewEvent.objects.filter(destination=destination)
            for event in events[1:]:  # Keep the first occurrence
                event.delete()
