# chatbrain.py
from memory.memory_manager import MemoryManager
from persona.mode_switcher import PersonaEngine

class ChatBrain:
    def __init__(self, channel_id="main"):
        self.channel_id = channel_id
        self.twitch_followers = 0
        self.memory = MemoryManager()
        self.persona_engine = PersonaEngine()

    def get_response(self, message, speaker=None, emotion=None):
        return f"[{emotion or 'neutral'}] You said: {message}"

    def speak(self, text, emotion="neutral"):
        print(f"[{emotion.upper()}] {text}")

    def handle_new_follower_event(self, count):
        print(f"[FOLLOWERS] Total followers: {count}")
