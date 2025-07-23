# discord_listener.py
# Discord voice listener with emotion parsing and speaker recognition

import os
import asyncio
import discord
from voice.emotion_detector import detect_emotion_from_audio
from core.chatbrain import ChatBrain

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", 0))
CHANNEL_NAME = os.getenv("DISCORD_VOICE_CHANNEL", "General")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)
chatbrain = ChatBrain(channel_id="discord")

@client.event
async def on_ready():
    print(f"[DISCORD] Logged in as {client.user}")
    guild = discord.utils.get(client.guilds, id=GUILD_ID)
    if not guild:
        print("[DISCORD] Guild not found.")
        return

    channel = discord.utils.get(guild.voice_channels, name=CHANNEL_NAME)
    if not channel:
        print("[DISCORD] Voice channel not found.")
        return

    vc = await channel.connect()
    print(f"[DISCORD] Connected to {channel.name}")

    while True:
        audio_data = await listen_to_voice(vc)
        if audio_data:
            speaker_id, emotion = detect_emotion_from_audio(audio_data)
            print(f"[VOICE] {speaker_id} sounds {emotion}")
            chatbrain.react_to_voice_emotion(speaker_id, emotion)

async def listen_to_voice(vc):
    # Placeholder for audio stream capture from Discord
    await asyncio.sleep(2)
    return b""  # Simulated silence (replace with real frame buffer)

if __name__ == "__main__":
    client.run(TOKEN)
