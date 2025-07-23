# twitch_listener_bot.py
import os
import sys
import asyncio
import subprocess
from dotenv import load_dotenv
from twitchio.ext import eventsub
from pyngrok import ngrok
from obs.obs_websocket_service import trigger_emotion_visual

from memory.memory_manager import MemoryManager
from persona.mode_switcher import PersonaEngine

load_dotenv()

class TwitchFollowerListener:
    def __init__(self, app_id, app_secret, channel_login, chatbrain_instance):
        self.app_id = app_id
        self.app_secret = app_secret
        self.channel_login = channel_login
        self.chatbrain = chatbrain_instance
        self.eventsub_client = None

    async def start(self):
        auth_token = os.getenv("NGROK_AUTH_TOKEN")
        if auth_token:
            ngrok.set_auth_token(auth_token)
            print("[NGROK] Auth token set.")
        else:
            print("[WARNING] NGROK_AUTH_TOKEN not found. Using temporary tunnel.")

        tunnel = ngrok.connect(8080, bind_tls=True)
        public_url = tunnel.public_url
        print(f"[NGROK] Public URL: {public_url}")

        self.eventsub_client = eventsub.EventSubClient(
            client_id=self.app_id,
            client_secret=self.app_secret,
            callback_route=f"{public_url}/eventsub/callback",
            port=8080
        )

        await self.eventsub_client.subscribe_channel_follows_v2(
            broadcaster=self.channel_login,
            moderator=self.channel_login
        )
        await self.eventsub_client.subscribe_channel_subscriptions(
            broadcaster=self.channel_login
        )
        await self.eventsub_client.subscribe_channel_points_redeemed(
            broadcaster=self.channel_login
        )

        @self.eventsub_client.event("channel.follow")
        async def on_follow(event):
            print(f"[TWITCH FOLLOWER] {event.user.name} followed!")
            self.chatbrain.twitch_followers += 1
            self.chatbrain.memory.update_viewer_tag(event.user.name, "supportive", 1, reason="follow")
            self.chatbrain.persona_engine.adjust_from_event("follow", event.user.name, weight=0.2)
            self.chatbrain.handle_new_follower_event(self.chatbrain.twitch_followers)
            trigger_emotion_visual("happy")

        @self.eventsub_client.event("channel.subscribe")
        async def on_sub(event):
            print(f"[TWITCH SUB] {event.user.name} subscribed!")
            self.chatbrain.memory.update_viewer_tag(event.user.name, "loyal", 2, reason="subscribed")
            self.chatbrain.persona_engine.adjust_from_event("subscribe", event.user.name, weight=0.3)
            self.chatbrain.speak(
                f"Thanks for subscribing, {event.user.name}! You're unlocking my true power.",
                "affection"
            )
            trigger_emotion_visual("happy")

        @self.eventsub_client.event("channel.channel_points_custom_reward_redemption.add")
        async def on_points(event):
            print(f"[TWITCH POINTS] {event.user.name} redeemed {event.reward.title}")
            self.chatbrain.speak(
                f"{event.user.name} redeemed {event.reward.title}. What chaos awaits?",
                "curious"
            )
            if "glitch" in event.reward.title.lower():
                trigger_emotion_visual("glitched")

        print("[TWITCH] EventSub listener active")
        await self.eventsub_client.listen()

def launch_additional_services():
    try:
        subprocess.Popen([sys.executable, "discord_relay.py"])
        subprocess.Popen([sys.executable, "obs_websocket_service.py"])
        print("[SERVICES] Additional services launched.")
    except Exception as e:
        print(f"[ERROR] Launching additional services: {e}")

if __name__ == "__main__":
    from core.chatbrain import ChatBrain

    app_id = os.getenv("TWITCH_APP_ID")
    app_secret = os.getenv("TWITCH_APP_SECRET")
    login = os.getenv("TWITCH_CHANNEL_LOGIN", "your_channel")

    brain = ChatBrain(channel_id="main")
    listener = TwitchFollowerListener(app_id, app_secret, login, brain)

    launch_additional_services()

    try:
        asyncio.run(listener.start())
    except KeyboardInterrupt:
        print("[EXIT] Shutting down Twitch listener.")
        sys.exit(0)
