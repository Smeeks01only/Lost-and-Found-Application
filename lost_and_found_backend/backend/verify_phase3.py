import sys
import os
import django
from django.conf import settings

# Setup Django Environment for standalone script
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from search_engine.services import VectorService
from lf_items.models import Item

def verify_phase3():
    print("Initializing VectorService...")
    service = VectorService.get_instance()
    
    # Check index size
    total_items = Item.objects.count()
    print(f"Total items in DB: {total_items}")
    print(f"Index size: {service.index.ntotal}")
    
    if service.index.ntotal != total_items:
        print("⚠️  Warning: Index size mismatch (might be due to previous deletes or non-sync)")
    
    # 1. Search Verification
    print("\nTest 1: Searching for 'black wallet'...")
    results = service.search("black wallet", k=3)
    print("Results:", results)
    
    found_wallet = False
    for item_id, score in results:
        item = Item.objects.get(id=item_id)
        print(f" - Found: {item.description} (Score: {score:.4f})")
        if "wallet" in item.description.lower():
            found_wallet = True
            
    if found_wallet:
        print("✅ Semantic Search Passed (Found wallet)")
    else:
        print("❌ Semantic Search Failed (Did not find wallet)")

if __name__ == "__main__":
    verify_phase3()
