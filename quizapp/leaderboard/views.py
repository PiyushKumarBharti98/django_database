# leaderboard/views.py
from rest_framework import generics
from .models import Leaderboard
from .serializers import LeaderboardSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class LeaderboardListCreateView(generics.ListCreateAPIView):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

class LeaderboardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

class GenreLeaderboardView(generics.ListAPIView):
    serializer_class = LeaderboardSerializer  # Specify the serializer class

    def get_queryset(self):
        genre = self.kwargs['genre']  # Get the genre from the URL
        return Leaderboard.objects.filter(genre=genre).order_by('-score')

class DeleteUserFromGenreView(APIView):
    def delete(self, request, genre, wallet_address):
        try:
            # Find the entry for the specified genre and wallet address
            entry = Leaderboard.objects.get(genre=genre, wallet_address=wallet_address)
            entry.delete()  # Delete the entry
            return Response(
                {"message": "User deleted successfully from the genre leaderboard."},
            )
        except Leaderboard.DoesNotExist:
            return Response(
                {"error": "User not found in the specified genre leaderboard."},
            )
