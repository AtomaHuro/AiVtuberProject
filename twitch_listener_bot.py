# twitch_listener_bot.py
# Twitch follower count + event listener using TwitchIO + EventSub + Ngrok support

from twitchio.ext import commands, eventsub
from pyngrok import ngrok
import os
from dotenv import load_dotenv
import asyncio

class TwitchFollowerListener:
    def __init__(self, app_id, app_secret, channel_login, chatbrain_instance):
        self.app_id = app_id
        self.app_secret = app_secret
        self.channel_login = channel_login
        self.chatbrain = chatbrain_instance
        self.eventsub_client = None

    async def start(self):
        # Authenticate and set up ngrok tunnel
        auth_token = os.getenv("NGROK_AUTH_TOKEN")
        if auth_token:
            ngrok.set_auth_token(auth_token)
            print("[NGROK] Auth token set.")
        else:
            print("[WARNING] NGROK_AUTH_TOKEN not found. Using temporary tunnel.")
        public_url = ngrok.connect(8080, bind_tls=True)
        print(f"[NGROK] Public URL: {public_url}")
        self.eventsub_client = eventsub.EventSubClient(
            client_id=self.app_id,
            client_secret=self.app_secret,
            callback_route=f"{public_url}/eventsub/callback",  # Replace with actual
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
            self.chatbrain.handle_new_follower_event(self.chatbrain.twitch_followers)

        @self.eventsub_client.event("channel.subscribe")
        async def on_sub(event):
            print(f"[TWITCH SUB] {event.user.name} subscribed!")
            self.chatbrain.speak(f"Thanks for subscribing, {event.user.name}! You're unlocking my true power.", "affection")

        @self.eventsub_client.event("channel.channel_points_custom_reward_redemption.add")
        async def on_points(event):
            print(f"[TWITCH POINTS] {event.user.name} redeemed {event.reward.title}")
            self.chatbrain.speak(f"{event.user.name} redeemed {event.reward.title}. What chaos awaits?", "curious")

                print("[TWITCH] EventSub listener active")
        await self.eventsub_client.listen()


# Load environment variables from .env file
    load_dotenv()

    if __name__ == "__main__":
    import sys
    from chatbrain_core import ChatBrain  # Adjust this path if needed

    # Example additional service hooks (OBS, Discord, etc.)
    def launch_additional_services():
        try:
            import subprocess
            # Example: Launch OBS WebSocket or Discord relay if needed
            subprocess.Popen(["python3", "discord_relay.py"])
            subprocess.Popen(["python3", "obs_websocket_service.py"])
            print("[SERVICES] Additional services launched.")
        except Exception as e:
            print(f"[ERROR] Launching additional services: {e}")

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
