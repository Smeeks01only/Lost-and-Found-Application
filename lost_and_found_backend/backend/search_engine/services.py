import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from django.conf import settings

# Path to store the FAISS index on disk
INDEX_FILE = os.path.join(settings.BASE_DIR, 'search_index.faiss')
MODEL_NAME = 'all-MiniLM-L6-v2'

class VectorService:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        print(f"Loading SBERT model: {MODEL_NAME}...")
        self.model = SentenceTransformer(MODEL_NAME)
        # Dimension for all-MiniLM-L6-v2 is 384
        self.dimension = 384 
        
        if os.path.exists(INDEX_FILE):
             print(f"Loading FAISS index from {INDEX_FILE}...")
             self.index = faiss.read_index(INDEX_FILE)
        else:
             print("Creating new FAISS index...")
             # IndexIDMap allows us to store arbitrary IDs (like our DB Item IDs)
             self.index = faiss.IndexIDMap(faiss.IndexFlatL2(self.dimension))

    def encode(self, text):
        """Converts text to a vector embedding."""
        if not text:
            return np.zeros(self.dimension, dtype='float32')
        return self.model.encode([text])[0]

    def add_item(self, item_id, text):
        """Adds an item's vector to the index with its DB ID."""
        vector = self.encode(text)
        vector_np = np.array([vector]).astype('float32')
        ids_np = np.array([item_id]).astype('int64')
        
        # If ID already exists, we should technically remove it first, 
        # but IndexIDMap doesn't support easy removal/update in checking existence effectively without loading. 
        # For this prototype, we'll just add. Real world would need remove_ids.
        try:
            self.index.remove_ids(ids_np)
        except:
            pass # ID might not exist
            
        self.index.add_with_ids(vector_np, ids_np)
        self.save_index()
        print(f"Indexed Item {item_id}")

    def search(self, text, k=5):
        """Searches for similar items."""
        vector = self.encode(text)
        vector_np = np.array([vector]).astype('float32')
        distances, ids = self.index.search(vector_np, k)
        # Filter out -1 ids (FAISS returns -1 if not enough neighbors)
        valid_results = []
        for id_val, dist in zip(ids[0], distances[0]):
            if id_val != -1:
                valid_results.append((int(id_val), float(dist)))
        return valid_results

    def save_index(self):
        """Persists the index to disk."""
        faiss.write_index(self.index, INDEX_FILE)
        
    def reset_index(self):
        """Clears the index."""
        self.index = faiss.IndexIDMap(faiss.IndexFlatL2(self.dimension))
        self.save_index()
