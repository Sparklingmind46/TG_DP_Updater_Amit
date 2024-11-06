# profile_picture_updater.py
from telethon import TelegramClient, functions
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import asyncio

# Load Telegram API credentials from environment variables
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

# Optional: Customize the image size and font
image_size = (512, 512)
font_size = 100
font_path = 'fonts/font-PiroHackz.ttf'  # Adjust based on your repo structure
font = ImageFont.truetype(font_path, font_size)

# Directory to save the generated image
image_file = 'current_time_pfp.png'

# Function to create an image with the current time
def create_time_image():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # Create an image with a white background
    image = Image.new("RGB", image_size, (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Load font and draw the text (current time)
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(current_time, font=font)
    text_position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)
    draw.text(text_position, current_time, font=font, fill=(0, 0, 0))

    # Save the image
    image.save(image_file)

async def update_profile_picture(client):
    while True:
        # Create the image with the current time
        create_time_image()

        # Update the profile picture
        print("Updating profile picture with current time...")
        await client(functions.photos.UploadProfilePhotoRequest(
            file=await client.upload_file(image_file)
        ))

        # Delete old profile photos
        await client(functions.photos.DeletePhotosRequest(
            await client.get_profile_photos('me')
        ))

        # Wait for 1 hour before updating again
        await asyncio.sleep(60)

async def main():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        # Continuously update the profile picture
        await update_profile_picture(client)

# Run the code
asyncio.run(main())
