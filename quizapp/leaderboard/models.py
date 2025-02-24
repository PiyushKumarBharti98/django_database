from django.db import models

class Leaderboard(models.Model):
    wallet_address = models.CharField(max_length=42)  # Ethereum wallet address
    genre = models.CharField(max_length=100)  
    score = models.IntegerField()  
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.wallet_address} - {self.genre} - {self.score}"

class GeneratedImage(models.Model):
    prompt = models.CharField(max_length=255)  
    image_url = models.URLField()             
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Image generated from prompt: {self.prompt}"

class UserProgress(models.Model):
    wallet_address = models.CharField(max_length=42)  
    genre = models.CharField(max_length=100) 
    prompt_index = models.IntegerField(default=0)  

    def __str__(self):
        return f"{self.wallet_address} - {self.genre} - Prompt {self.prompt_index}"

class WalletMetadata(models.Model):
    wallet_address = models.CharField(max_length=42, unique=True) 
    metadata = models.JSONField()  

    def __str__(self):
        return f"{self.wallet_address} - {self.metadata}"
