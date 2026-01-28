from rest_framework import generics, permissions
from django.db.models import Q
from .models import PotentialMatch
from .serializers import PotentialMatchSerializer

class MatchListView(generics.ListAPIView):
    serializer_class = PotentialMatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Return matches where the user is either the loser OR the finder (if we track finder identity)
        # Assuming 'reporter' on Item is the relevant user.
        return PotentialMatch.objects.filter(
            Q(lost_item__reporter=user) | Q(found_item__reporter=user)
        ).order_by('-created_at')
