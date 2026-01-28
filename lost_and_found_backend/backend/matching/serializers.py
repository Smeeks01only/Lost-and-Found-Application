from rest_framework import serializers
from .models import PotentialMatch
from lf_items.serializers import ItemSerializer

class PotentialMatchSerializer(serializers.ModelSerializer):
    # Nest the full item details so the UI can show them
    lost_item = ItemSerializer(read_only=True)
    found_item = ItemSerializer(read_only=True)

    class Meta:
        model = PotentialMatch
        fields = ['id', 'lost_item', 'found_item', 'score', 'status', 'created_at']
