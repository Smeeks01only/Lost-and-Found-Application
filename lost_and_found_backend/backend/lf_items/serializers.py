from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    reporter_username = serializers.ReadOnlyField(source='reporter.username')

    class Meta:
        model = Item
        fields = [
            'id', 'reporter', 'reporter_username', 'item_type', 'description', 
            'location', 'date_lost_found', 'status', 'contact_info',
            'security_question', 'created_at'
        ]
        read_only_fields = ['id', 'reporter', 'created_at', 'status']

class LostItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['description', 'location', 'date_lost_found', 'contact_info']

    def create(self, validated_data):
        validated_data['item_type'] = 'LOST'
        validated_data['reporter'] = self.context['request'].user
        return super().create(validated_data)

class FoundItemCreateSerializer(serializers.ModelSerializer):
    security_answer = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Item
        fields = [
            'description', 'location', 'date_lost_found', 'contact_info',
            'security_question', 'security_answer'
        ]

    def create(self, validated_data):
        security_answer = validated_data.pop('security_answer')
        validated_data['item_type'] = 'FOUND'
        validated_data['reporter'] = self.context['request'].user
        
        item = Item(**validated_data)
        item.set_security_answer(security_answer)
        item.save()
        return item
