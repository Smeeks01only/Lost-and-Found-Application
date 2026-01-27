from django.urls import path
from .views import LostItemListCreateView, FoundItemListCreateView, UserItemListView

urlpatterns = [
    path('lost/', LostItemListCreateView.as_view(), name='lost-items-list-create'),
    path('found/', FoundItemListCreateView.as_view(), name='found-items-list-create'),
    path('mine/', UserItemListView.as_view(), name='user-items-list'),
]
