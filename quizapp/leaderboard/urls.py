# leaderboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('leaderboard/', views.LeaderboardListCreateView.as_view(), name='leaderboard-list-create'),
    path('leaderboard/<int:pk>/', views.LeaderboardDetailView.as_view(), name='leaderboard-detail'),
    path('leaderboard/<str:genre>/', views.GenreLeaderboardView.as_view(), name='genre-leaderboard'),
]