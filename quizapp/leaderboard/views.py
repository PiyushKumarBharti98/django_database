## leaderboard/views.py
from rest_framework import generics
from .models import Leaderboard
from .serializers import LeaderboardSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProgress, GeneratedImage
from .scripts.generate_images import generate_image
from .models import GeneratedImage
from rest_framework.response import Response
from .models import WalletMetadata

class RetrieveWalletMetadataView(APIView):
    def get(self, request, wallet_address):
        try:
            wallet_metadata = WalletMetadata.objects.get(wallet_address=wallet_address)
            # Return only the metadata (e.g., image and description)
            return Response(wallet_metadata.metadata, status=status.HTTP_200_OK)
        except WalletMetadata.DoesNotExist:
            return Response(
                {"error": "Wallet address not found."},
                status=status.HTTP_404_NOT_FOUND
            )
from .serializers import GeneratedImageSerializer


class LeaderboardListCreateView(generics.ListCreateAPIView):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

class LeaderboardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

class GenreLeaderboardView(APIView):
    def get(self, request, genre):
        # Calculate the total score for each user in the specified genre
        leaderboard = Leaderboard.objects.filter(genre=genre).values('wallet_address').annotate(
            total_score=Sum('score')
        ).order_by('-total_score')

        return Response(leaderboard, status=status.HTTP_200_OK)

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

class AddQuizAttemptView(APIView):
    def post(self, request):
        serializer = LeaderboardSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new quiz attempt
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# leaderboard/views.py
from django.db.models import Sum

class UserTotalScoreView(APIView):
    def get(self, request, wallet_address, genre):
        # Calculate the total score for the user in the specified genre
        total_score = Leaderboard.objects.filter(
            wallet_address=wallet_address,
            genre=genre
        ).aggregate(total_score=Sum('score'))['total_score']

        if total_score is None:
            return Response(
                {"error": "No quiz attempts found for the specified user and genre."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"wallet_address": wallet_address, "genre": genre, "total_score": total_score},
            status=status.HTTP_200_OK
        )

class GeneratedImageView(APIView):
    def get(self, request):
        images = GeneratedImage.objects.all()
        serializer = GeneratedImageSerializer(images, many=True)
        return Response(serializer.data)

class AttemptQuizView(APIView):
    def post(self, request):
        wallet_address = request.data.get('wallet_address')
        genre = request.data.get('genre')

        if not wallet_address or not genre:
            return Response(
                {"error": "wallet_address and genre are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate the image
        generated_image = generate_image(wallet_address, genre)

        if not generated_image:
            return Response(
                {"error": "No more prompts available for this genre."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "message": "Quiz attempted successfully.",
                "image_url": generated_image.image_url,  # Return the Cloudinary URL
                "prompt": generated_image.prompt,
                "genre": genre
            },
            status=status.HTTP_201_CREATED
        )

from .models import WalletMetadata
from .serializers import WalletMetadataSerializer

class StoreWalletMetadataView(APIView):
    def post(self, request):
        serializer = WalletMetadataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveWalletMetadataView(APIView):
    def get(self, request, wallet_address):
        try:
            wallet_metadata = WalletMetadata.objects.get(wallet_address=wallet_address)
            # Return only the metadata (e.g., image and description)
            return Response(wallet_metadata.metadata, status=status.HTTP_200_OK)
        except WalletMetadata.DoesNotExist:
            return Response(
                {"error": "Wallet address not found."},
                status=status.HTTP_404_NOT_FOUND
            )
