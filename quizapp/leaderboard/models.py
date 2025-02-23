# leaderboard/models.py
from django.db import models

class Leaderboard(models.Model):
    wallet_address = models.CharField(max_length=42)  # Ethereum wallet address
    genre = models.CharField(max_length=100)  # Genre of the quiz (e.g., "Harry Potter")
    score = models.IntegerField()  # Score for this specific quiz attempt
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the quiz attempt

    def __str__(self):
        return f"{self.wallet_address} - {self.genre} - {self.score}"

class GeneratedImage(models.Model):
    prompt = models.CharField(max_length=255)  # Store the prompt used to generate the image
    image_url = models.URLField()              # Store the Cloudinary URL
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation

    def __str__(self):
        return f"Image generated from prompt: {self.prompt}"

class UserProgress(models.Model):
    wallet_address = models.CharField(max_length=42)  # User's wallet address
    genre = models.CharField(max_length=100)  # Genre of the quiz (e.g., "Harry Potter")
    prompt_index = models.IntegerField(default=0)  # Track the current prompt index

    def __str__(self):
        return f"{self.wallet_address} - {self.genre} - Prompt {self.prompt_index}"

class WalletMetadata(models.Model):
    wallet_address = models.CharField(max_length=42, unique=True)  # Ethereum wallet address
    metadata = models.JSONField()  # Store metadata as JSON

    def __str__(self):
        return f"{self.wallet_address} - {self.metadata}"
