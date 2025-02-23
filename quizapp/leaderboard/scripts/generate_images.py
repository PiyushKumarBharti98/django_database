# leaderboard/scripts/generate_image.py
import os
import io
from django.core.files import File
from PIL import Image
import cloudinary 
import cloudinary.uploader
import random
from .prompts import harry_potter_prompts , lord_of_the_rings_prompts , marvel_prompts
from huggingface_hub import InferenceClient
from leaderboard.models import UserProgress, GeneratedImage

# leaderboard/scripts/generate_image.py
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = InferenceClient(
    provider="hf-inference",
    api_key="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"
)

def generate_image(wallet_address, genre):
    try:
        # Get or create user progress
        user_progress, created = UserProgress.objects.get_or_create(
            wallet_address=wallet_address,
            genre=genre
        )
        logger.debug(f"User progress: {user_progress}")

        # Get the random prompt index
        prompt_index = random.randint(0,7)
        logger.debug(f"Prompt index: {prompt_index}")

        # Select the appropriate prompt list
        if genre == "Harry Potter":
            prompts = harry_potter_prompts
        elif genre == "Marvel":
            prompts = marvel_prompts
        elif genre == "Lord of the Rings":
            prompts = lord_of_the_rings_prompts
        else:
            raise ValueError("Invalid genre")

        # Get the current prompt
        prompt = prompts[prompt_index]
        logger.debug(f"Current prompt: {prompt}")

        # Generate the image
        image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-dev"
        )
        logger.debug(f"Image data type: {type(image)}")
        #logger.debug(f"Image data length: {len(image)}")

        # Convert the image to a PIL Image object
        pil_image = image
        logger.debug(f"PIL image format: {pil_image.format}")
        logger.debug(f"PIL image size: {pil_image.size}")

        # Convert the PIL Image to bytes
        img_byte_array = io.BytesIO()
        pil_image.save(img_byte_array, format='PNG')  # Save as PNG
        img_byte_array.seek(0)
        logger.debug(f"Image bytes length: {len(img_byte_array.getvalue())}")

        # Upload the image to Cloudinary
        upload_result = cloudinary.uploader.upload(
            img_byte_array,  # Pass the bytes-like object
            folder="quizapp",  # Optional: Organize images in a folder
            public_id=f"{genre}_{wallet_address}_{prompt_index}"  # Unique ID for the image
        )
        logger.debug(f"Image uploaded to Cloudinary: {upload_result}")

        # Save the image URL to the database
        generated_image = GeneratedImage(
            prompt=prompt,
            image_url=upload_result['secure_url']  # Save the Cloudinary URL
        )
        generated_image.save()
        logger.debug(f"Generated image saved to database: {generated_image}")

        # Update the user's progress
        user_progress.prompt_index += 1
        user_progress.save()
        logger.debug(f"User progress updated: {user_progress}")

        return generated_image

    except Exception as e:
        logger.error(f"Error in generate_image: {e}")
        raise
