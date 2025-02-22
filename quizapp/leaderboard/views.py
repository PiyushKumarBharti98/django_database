# leaderboard/views.py
from rest_framework import generics
from .models import Leaderboard
from .serializers import LeaderboardSerializer
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