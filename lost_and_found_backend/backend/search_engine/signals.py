from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from lf_items.models import Item
from .services import VectorService
import numpy as np

@receiver(post_save, sender=Item)
def update_item_index(sender, instance, **kwargs):
    """Updates the FAISS index when an item is saved."""
    print(f"Signal received: Indexing Item {instance.id}")
    service = VectorService.get_instance()
    
    # Enrich text with metadata for better matching
    text_to_encode = f"{instance.get_item_type_display()} Item. Description: {instance.description}. Location: {instance.location}"
    
    service.add_item(instance.id, text_to_encode)

@receiver(post_delete, sender=Item)
def remove_item_index(sender, instance, **kwargs):
    """Removes the item from FAISS index when deleted."""
    print(f"Signal received: Removing Item {instance.id}")
    service = VectorService.get_instance()
    try:
        ids_np = np.array([instance.id]).astype('int64')
        service.index.remove_ids(ids_np)
        service.save_index()
    except Exception as e:
        print(f"Error removing item {instance.id}: {e}")
