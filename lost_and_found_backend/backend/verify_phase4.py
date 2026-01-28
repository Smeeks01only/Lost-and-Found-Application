import sys
import os
import django
import datetime

# Setup Django Environment for standalone script
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from lf_items.models import Item
from matching.models import PotentialMatch
from django.contrib.auth import get_user_model
from search_engine.services import VectorService

User = get_user_model()

def verify_phase4():
    print("Preparing Matching Test...")
    
    # 1. Setup User
    user, _ = User.objects.get_or_create(username="matching_tester")
    
    # 2. Clear old data for cleaner test
    PotentialMatch.objects.all().delete()
    Item.objects.all().delete()
    
    # 3. Create LOST Item
    print("Creating LOST Item: 'Silver Hp Laptop'")
    lost_item = Item.objects.create(
        reporter=user,
        item_type='LOST',
        description="Lost my Silver HP Elitebook laptop in the cafeteria.",
        location="Cafeteria",
        date_lost_found=datetime.datetime.now(),
        contact_info="lost@example.com"
    )
    
    # 4. Create FOUND Item (Good Match)
    print("Creating FOUND Item: 'Silver HP Laptop'")
    found_item_match = Item.objects.create(
        reporter=user,
        item_type='FOUND',
        description="Found a silver HP laptop on a table.",
        location="Cafeteria",
        date_lost_found=datetime.datetime.now(),
        contact_info="found@example.com"
    )
    
    # 5. Create FOUND Item (No Match)
    print("Creating FOUND Item: 'Red Umbrella' (Distractor)")
    found_item_no_match = Item.objects.create(
        reporter=user,
        item_type='FOUND',
        description="Found a red umbrella near the exit.",
        location="Exit",
        date_lost_found=datetime.datetime.now(),
        contact_info="found@example.com"
    )
    
    # 6. Ensure they are indexed (Signals should have done this, but verify size)
    service = VectorService.get_instance()
    print(f"Index size: {service.index.ntotal} (Expected >= 3)")

    # 7. Run Matching Job logic directly
    print("\nRunning Matching Command Logic...")
    from matching.services import MatchingService
    match_service = MatchingService()
    
    # Run for lost item
    match_service.find_matches_for_item(lost_item)
    
    # 8. Check Results
    matches = PotentialMatch.objects.filter(lost_item=lost_item)
    print(f"\nMatches found for Lost Item: {matches.count()}")
    
    found_correct = False
    for m in matches:
        print(f" - Match: {m.found_item.description} (Score: {m.score:.4f})")
        if m.found_item.id == found_item_match.id:
            found_correct = True
            
    if found_correct:
        print("✅ SUCCESS: Correct match identified!")
    else:
        print("❌ FAILURE: Correct match NOT identified.")

if __name__ == "__main__":
    verify_phase4()
