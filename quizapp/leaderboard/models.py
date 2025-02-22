# leaderboard/models.py
from django.db import models

class Leaderboard(models.Model):
    wallet_address = models.CharField(max_length=42, unique=False)  # Ethereum wallet address
    genre = models.CharField(max_length=100)  # Genre of the quiz (e.g., "Harry Potter")
    score = models.IntegerField()  # User's score
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the quiz attempt

    class Meta:
        unique_together = ('wallet_address', 'genre')  # Ensure one score per wallet per genre

    def __str__(self):
        return f"{self.wallet_address} - {self.genre} - {self.score}"