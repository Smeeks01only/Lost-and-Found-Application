from django.core.management.base import BaseCommand
from lf_items.models import Item
from search_engine.services import VectorService

class Command(BaseCommand):
    help = 'Rebuilds the FAISS index from all existing items'

    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing VectorService...")
        service = VectorService.get_instance()
        
        self.stdout.write("Clearing existing index...")
        service.reset_index()
        
        items = Item.objects.all()
        count = items.count()
        self.stdout.write(f"Found {count} items to index.")
        
        for item in items:
            text = f"{item.get_item_type_display()} Item. Description: {item.description}. Location: {item.location}"
            service.add_item(item.id, text)
            self.stdout.write(f"Indexed Item {item.id}")
            
        self.stdout.write(self.style.SUCCESS(f"Successfully indexed {count} items."))
