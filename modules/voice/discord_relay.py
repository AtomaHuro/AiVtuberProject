# discord_relay.py
# Receives Discord voice input and relays emotional data to ChatBrain

import os
import asyncio
import discord
from voice.emotion_detector import detect_emotion
from core.chatbrain import ChatBrain

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

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    emotion = detect_emotion(message.content)
    print(f"[DISCORD] {message.author}: {message.content} -> {emotion}")
    response = chatbrain.get_response(message.content, speaker=message.author.name, emotion=emotion)
    chatbrain.speak(response, emotion)

# Token from .env or config
client.run(os.getenv("DISCORD_BOT_TOKEN"))
