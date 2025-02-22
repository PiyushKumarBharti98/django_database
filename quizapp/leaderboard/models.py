# leaderboard/models.py
from django.db import models

class Leaderboard(models.Model):
    wallet_address = models.CharField(max_length=42)  # Ethereum wallet address
    genre = models.CharField(max_length=100)  # Genre of the quiz (e.g., "Harry Potter")
    score = models.IntegerField()  # Score for this specific quiz attempt
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the quiz attempt

    def __str__(self):
        return f"{self.wallet_address} - {self.genre} - {self.score}"
