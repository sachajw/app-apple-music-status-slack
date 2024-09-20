import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Apple Music and Slack credentials
APPLE_MUSIC_API_KEY = os.getenv('APPLE_MUSIC_API_KEY')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_CHANNEL_ID = os.getenv('SLACK_CHANNEL_ID')
APPLE_MUSIC_USER_TOKEN = os.getenv('APPLE_MUSIC_USER_TOKEN')

# Initialize Slack client
slack_client = WebClient(token=SLACK_BOT_TOKEN)

def get_currently_playing_song():
    """Fetch the currently playing song from Apple Music."""
    url = "https://api.music.apple.com/v1/me/recent/played"
    headers = {
        "Authorization": f"Bearer {APPLE_MUSIC_API_KEY}",
        "Music-User-Token": APPLE_MUSIC_USER_TOKEN
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data and data['data']:
            # Extract the song details
            song = data['data'][0]['attributes']
            song_name = song['name']
            artist_name = song['artistName']
            return f"🎵 Now Playing: {song_name} by {artist_name}"
        else:
            return "No song is currently playing."
    else:
        return "Failed to fetch currently playing song."

def post_to_slack(message):
    """Post a message to the configured Slack channel."""
    try:
        response = slack_client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            text=message
        )
        print(f"Message posted to Slack: {response['message']['text']}")
    except SlackApiError as e:
        print(f"Failed to post message: {e.response['error']}")

if __name__ == "__main__":
    song_info = get_currently_playing_song()
    post_to_slack(song_info)
