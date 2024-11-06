# profile_picture_updater.py
from telethon import TelegramClient, events
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
from flask import Flask
from threading import Thread
import time

# Initialize Flask app for health check
app = Flask(__name__)

@app.route('/')
def health_check():
    return "OK", 200  # Koyeb expects this response to confirm health

def run_flask():
    app.run(host="0.0.0.0", port=8000)

# Your Telegram bot credentials and other logic
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_number = "YOUR_PHONE_NUMBER"  # Replace with your phone number

client = TelegramClient("session_name", api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    # Handle incoming messages or updates
    pass

def update_pfp():
    # Get current time in 12-hour format with AM/PM and no seconds
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")  # Format: Hour:Minute AM/PM (no seconds)
    
    # Create an image with a white background (512x512)
    image = Image.new("RGB", (512, 512), (255, 255, 255))  # white background
    draw = ImageDraw.Draw(image)
    
    # Try to load a custom font, if available, or fall back to default
    try:
        font_path = "fonts/font-PiroHackz.ttf"  # Specify the path to your .ttf font file
        font = ImageFont.truetype(font_path, 40)
    except IOError:
        font = ImageFont.load_default()

    # Calculate the text size and position it in the center for the time
    text_width, text_height = draw.textsize(time_str, font)
    draw.text(((512 - text_width) / 2, (512 - text_height) / 3), time_str, fill="black", font=font)  # black font

    # Now draw "Amit" in tiny letters below the time
    try:
        small_font = ImageFont.truetype(font_path, 20)  # Smaller font for "Amit"
    except IOError:
        small_font = ImageFont.load_default()

    # Calculate the text size for "Amit" and position it below the time
    small_text_width, small_text_height = draw.textsize("Amit", small_font)
    draw.text(((512 - small_text_width) / 2, (512 - text_height + small_text_height) / 1.5), "- Amit", fill="black", font=small_font)

    # Save the image
    image.save("profile_picture.png")

    # Update the Telegram profile picture
    client.loop.run_until_complete(client.update_profile(photo="profile_picture.png"))

    # Delete the image after updating
    os.remove("profile_picture.png")

# Start the Flask server in a separate thread
thread = Thread(target=run_flask)
thread.start()

if __name__ == "__main__":
    # Start the Telegram bot client
    client.start()
    
    # Run the bot and continuously update the profile picture
    while True:
        update_pfp()
        time.sleep(60)  # Update every 60 seconds (1 minute)
