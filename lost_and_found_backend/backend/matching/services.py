from lf_items.models import Item
from search_engine.services import VectorService
from .models import PotentialMatch
from django.db import transaction

class MatchingService:
    def __init__(self):
        self.vector_service = VectorService.get_instance()
        self.similarity_threshold = 0.5  # Tunable threshold

    def find_matches_for_item(self, item):
        """
        Finds matches for a single item.
        If item is LOST, looks for FOUND.
        If item is FOUND, looks for LOST.
        """
        print(f"Running matching for {item} ({item.item_type})...")
        
        # 1. Search vector DB
        # text to search is the item's description + enriched data
        query_text = f"{item.get_item_type_display()} Item. Description: {item.description}. Location: {item.location}"
        
        # We ask for top 10 candidates
        candidates = self.vector_service.search(query_text, k=10)
        
        match_count = 0
        target_type = 'FOUND' if item.item_type == 'LOST' else 'LOST'

        for other_id, score in candidates:
            # Low score means high distance in Euclidean (L2), 
            # OR high score means high similarity in Cosine?
            # FAISS IndexFlatL2 returns Squared L2 Distance.
            # Lower is better. 0 is identical.
            # We need to interpret the score based on the index type. 
            # Our VectorService uses IndexFlatL2.
            # Let's assume a customized "threshold" based on observation.
            # For L2, let's say < 1.0 is a decent match for normalized vectors, 
            # but SBERT vectors aren't unit length by default unless normalized.
            # Wait, SBERT .encode() output is usually normalized? 
            # checked doc: SentenceTransformer.encode default normalize_embeddings=False.
            # However, for 'all-MiniLM-L6-v2', they are often used with Cosine Similarity.
            # If using L2: Distance = 2 * (1 - CosineSimilarity) for normalized vectors.
            # Use distance threshold e.g. 1.0 (corresponds to cosine sim 0.5)
            
            # For prototype, let's trust the top K and just filter strictly by DB type/status.
            
            try:
                other_item = Item.objects.get(id=other_id)
            except Item.DoesNotExist:
                continue

            # Must match target type
            if other_item.item_type != target_type:
                continue
                
            # Must be active
            if other_item.status != 'ACTIVE':
                continue

            # Avoid self-matching (unlikely with type check but safe)
            if item.id == other_item.id:
                continue

            # Identify which is lost/found for the record
            if item.item_type == 'LOST':
                lost, found = item, other_item
            else:
                lost, found = other_item, item

            # Create/Update PotentialMatch
            # Use get_or_create to avoid duplicates
            pm, created = PotentialMatch.objects.get_or_create(
                lost_item=lost,
                found_item=found,
                defaults={'score': float(score)}
            )
            
            if created:
                print(f" >> Created Match: {lost.id} <-> {found.id} (Score: {score})")
                match_count += 1
            else:
                 # Update score if it changed significantly?
                 # For now, ignore.
                 pass

        return match_count
