# leaderboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('leaderboard/', views.LeaderboardListCreateView.as_view(), name='leaderboard-list-create'),
    path('leaderboard/<int:pk>/', views.LeaderboardDetailView.as_view(), name='leaderboard-detail'),
    path('leaderboard/<str:genre>/', views.GenreLeaderboardView.as_view(), name='genre-leaderboard'),
    path('leaderboard/<str:genre>/delete/<str:wallet_address>/', views.DeleteUserFromGenreView.as_view(), name='delete-user-from-genre'),
     path('add-attempt/', views.AddQuizAttemptView.as_view(), name='add-quiz-attempt'),
    path('total-score/<str:wallet_address>/<str:genre>/', views.UserTotalScoreView.as_view(), name='user-total-score'),
]
