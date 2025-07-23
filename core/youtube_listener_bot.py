# youtube_listener_bot.py
# YouTube Live Chat listener for reactions and persona/memory logic

import os
import asyncio
from core.chatbrain import ChatBrain

# This requires an external API or YouTube chat polling
# Placeholder setup assuming polling loop from live chat

class YouTubeChatListener:
    def __init__(self, live_chat_id, chatbrain_instance):
        self.live_chat_id = live_chat_id
        self.chatbrain = chatbrain_instance

    async def poll_chat(self):
        print("[YOUTUBE] Starting live chat poll loop...")
        while True:
            messages = await self.fetch_new_messages()
            for msg in messages:
                user = msg["author"]
                text = msg["text"]
                print(f"[YT] {user}: {text}")
                self.chatbrain.process_viewer_message(user, text, platform="youtube")
            await asyncio.sleep(5)

    async def fetch_new_messages(self):
        return []  # Replace with actual chat fetch

if __name__ == "__main__":
    live_chat_id = os.getenv("YOUTUBE_LIVE_CHAT_ID")
    brain = ChatBrain(channel_id="youtube")
    listener = YouTubeChatListener(live_chat_id, brain)

    try:
        asyncio.run(listener.poll_chat())
    except KeyboardInterrupt:
        print("[YOUTUBE] Listener stopped.")
