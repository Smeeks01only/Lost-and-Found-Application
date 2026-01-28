from django.core.management.base import BaseCommand
from lf_items.models import Item
from matching.services import MatchingService

class Command(BaseCommand):
    help = 'Runs the matching algorithm on all active items'

    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing MatchingService...")
        service = MatchingService()
        
        # Iterate over all active items
        # In a real production job, we'd flag items that have already been fully processed
        # or only process new ones. For now, we scan everything active.
        items = Item.objects.filter(status='ACTIVE')
        total_matches = 0
        
        self.stdout.write(f"Scanning {items.count()} active items for matches...")
        
        for item in items:
            matches_found = service.find_matches_for_item(item)
            if matches_found > 0:
                self.stdout.write(f" + Found {matches_found} matches for Item {item.id}")
                total_matches += matches_found
                
        self.stdout.write(self.style.SUCCESS(f"Matching job complete. Created {total_matches} new potential matches (bi-directional potentially)."))
