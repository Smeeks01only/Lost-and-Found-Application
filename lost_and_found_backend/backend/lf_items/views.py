from rest_framework import generics, permissions
from .models import Item
from .serializers import ItemSerializer, LostItemCreateSerializer, FoundItemCreateSerializer

class LostItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Item.objects.filter(item_type='LOST').order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LostItemCreateSerializer
        return ItemSerializer

class FoundItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(item_type='FOUND').order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FoundItemCreateSerializer
        return ItemSerializer

class UserItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(reporter=self.request.user).order_by('-created_at')
