from django.db import models
from lf_items.models import Item

class PotentialMatch(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )

    # We link two items: one lost, one found.
    # We can enforce that item_a is LOST and item_b is FOUND, 
    # but for flexibility we'll name them specifically.
    lost_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='potential_matches_as_lost')
    found_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='potential_matches_as_found')
    
    score = models.FloatField(help_text="Similarity score from Vector Search")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('lost_item', 'found_item')
        ordering = ['score']

    def __str__(self):
        return f"Match ({self.score:.2f}): {self.lost_item} <-> {self.found_item}"
