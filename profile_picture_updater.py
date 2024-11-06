# profile_picture_updater.py
from flask import Flask
from telethon import TelegramClient
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import asyncio
import time
import requests
from io import BytesIO

# Initialize Flask app
app = Flask(__name__)

# Telethon API credentials
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")

# Initialize Telethon client
client = TelegramClient("session_name", api_id, api_hash)

# Health check route for Koyeb
@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200

# Function to create profile picture with custom background from URL
async def create_profile_picture():
    # URL for custom background image (replace with your image URL)
    background_url = os.getenv("BACKGROUND_URL", "https://example.com/background.jpg")

    try:
        # Download the background image from the web
        response = requests.get(background_url)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx errors
        background = Image.open(BytesIO(response.content))  # Open image from downloaded content
        background = background.resize((640, 640))  # Resize to match profile picture dimensions

        # Prepare text (current time and "Amit")
        current_time = datetime.now().strftime("%I:%M %p")  # Current time with AM/PM
        draw = ImageDraw.Draw(background)

        # Specify font paths for time and "Amit" text
        font = ImageFont.truetype("fonts/font-PiroHackz.ttf", 120)  # Adjust font path
        small_font = ImageFont.truetype("fonts/font-PiroHackz.ttf", 40)  # Small font for "Amit"

        # Draw the current time
        text_width, text_height = draw.textsize(current_time, font=font)
        draw.text(((640 - text_width) / 2, 200), current_time, fill="black", font=font)

        # Draw the "Amit" text
        amit_width, amit_height = draw.textsize("Amit", font=small_font)
        draw.text(((640 - amit_width) / 2, 350), "Amit", fill="black", font=small_font)

        # Save the final image
        background.save("profile_picture.png")
        print("Profile picture created and saved with custom background.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading background image: {e}")

# Function to update Telegram profile picture
async def update_pfp():
    while True:  # Run indefinitely with a sleep interval
        await create_profile_picture()
        try:
            # Delete the previous profile picture first
            await client.delete_profile_photo()  # This deletes the old profile picture
            print("Old profile picture deleted successfully.")

            # Update the profile picture with the new one
            await client.update_profile(photo="profile_picture.png")
            print("Profile picture updated successfully.")
        except Exception as e:
            print(f"Error updating profile picture: {e}")
        
        # Sleep for the defined interval before the next update (in seconds)
        sleep_interval = int(os.getenv("SLEEP_INTERVAL", 60))  # Default to 60 seconds
        print(f"Sleeping for {sleep_interval} seconds before the next update...")
        await asyncio.sleep(sleep_interval)  # Sleep for the specified interval

# Start Telethon client and update profile picture
@app.before_first_request
def start_telethon():
    asyncio.ensure_future(client.start())  # Start Telethon client
    asyncio.ensure_future(update_pfp())    # Start the profile picture update loop

# Run Flask app to handle health checks
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
