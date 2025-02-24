from rest_framework import serializers
from .models import Leaderboard
from .models import GeneratedImage

class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ['wallet_address', 'genre', 'score', 'timestamp']

class GeneratedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedImage
        fields = ['id', 'prompt', 'image', 'created_at']

from .models import WalletMetadata

class WalletMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletMetadata
        fields = ['wallet_address', 'metadata']
