from django.db import models
from django.conf import settings
import hashlib

class Item(models.Model):
    ITEM_TYPES = (
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
    )
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('CLAIMED', 'Claimed'),
        ('ARCHIVED', 'Archived'),
    )

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_items')
    item_type = models.CharField(max_length=5, choices=ITEM_TYPES)
    description = models.TextField(help_text="Detailed description of the item")
    location = models.CharField(max_length=255, help_text="Where it was lost or found")
    date_lost_found = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    
    # Security mechanism for FOUND items
    security_question = models.CharField(max_length=255, blank=True, null=True, help_text="Question for verifying ownership")
    security_answer_hash = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_security_answer(self, answer):
        """Hashes and sets the security answer."""
        if answer:
            self.security_answer_hash = hashlib.sha256(answer.lower().strip().encode('utf-8')).hexdigest()

    def check_security_answer(self, answer):
        """Verifies the security answer."""
        if not answer:
            return False
        input_hash = hashlib.sha256(answer.lower().strip().encode('utf-8')).hexdigest()
        return input_hash == self.security_answer_hash

    def __str__(self):
        return f"{self.item_type}: {self.description[:30]}..."
