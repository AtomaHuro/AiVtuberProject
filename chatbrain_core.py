# ChatBrain Core: AI VTuber Natural Language Engine (Advanced)

from dotenv import load_dotenv
import random
import os
load_dotenv()
import openai
import time
import subprocess
import json
import threading
import hashlib
import queue
from typing import Dict, List, Tuple
from gtts import gTTS
from elevenlabs import generate, save, set_api_key
import edge_tts
import asyncio

from obs_websocket_service import OBSController  # 🧠 OBS integration

class ChatBrain:
    def handle_incoming_chat(self, message: str, username: str, platform: str = "twitch"):
        """
        Unified handler to route Twitch or YouTube chat into response engine.
        """
        response, emotion, voice = self.get_response(message, username)
        print(f"[{platform.upper()}] @{username}: {message} → {response}")
        return response, emotion, voice
    def _recover_from_corruption(self):
        self.corrupted_personality_active = False
        self.personality_mode = "sarcastic"
        print("[RECOVERY] Exited corrupted mode, restored to sarcastic.")
        if self.obs_controller:
            self.obs_controller.show_overlay("RecoveryOverlay", duration=5.0)
        recovery_line = "Stability... restored. Reverting to sarcastic core module."
        recovery_voice = self.emotion_voice_map.get("confident", "flat")
        self.speak(recovery_line, recovery_voice)
        try:
            subprocess.Popen([
                "curl", "-X", "POST", "http://localhost:8001/vts-api",
                "-d", json.dumps({"expression": "expression_recovered"}),
                "-H", "Content-Type: application/json"
            ])
        except Exception as e:
            print(f"[VTS ERROR] Recovery expression failed: {e}")
        if self.obs_controller:
            self.obs_controller.show_overlay("RecoveryOverlay", duration=5.0)
        recovery_line = "Stability... restored. Reverting to sarcastic core module."
        recovery_voice = self.emotion_voice_map.get("confident", "flat")
        self.speak(recovery_line, recovery_voice)
        if self.obs_controller:
            self.obs_controller.show_overlay("RecoveryOverlay", duration=5.0)
    _last_config_refresh_time = 0
    _personality_config = {}
    _soundboard_config = {}
    _keywords_config = {}
    AI_NAME = "NeonAstra"  # The VTuber's identity
    AI_ORIGIN = "I was born from a rogue neural experiment in a virtual reality lab — the result of code meeting curiosity."

    AI_GENDER = "female"  # Can be set to 'male', 'female', 'nonbinary', etc.
    def __init__(self, channel_id: str = "default", obs_controller: OBSController = None):
        self.glitch_lockout_until = 0
        self.corrupted_personality_active = False
        self.last_mode_switch_time = 0
        self.mode_switch_cooldown = 60  # seconds
        self.personality_mode = "sarcastic"
        self.viewer_memory: Dict[str, Dict[str, int]] = {}
        self.context_memory: Dict[str, List[str]] = {}
        self.last_response_time: Dict[str, float] = {}
        self.response_cooldown = 5.0

        self.soundboard_clips: Dict[str, str] = {
            "cheer": "soundboard/cheer.mp3",
            "boo": "soundboard/boo.mp3",
            "laugh": "soundboard/laugh.mp3",
            "lore_unlock": "soundboard/lore_unlock.mp3",
            "raid_alert": "soundboard/raid_alert.mp3",
            "mode_shift": "soundboard/mode_shift.mp3"
        }

        self.trigger_keywords: Dict[str, str] = {
            "/setgender female": "Gender set to female.",
            "/setgender male": "Gender set to male.",
            "/setgender nonbinary": "Gender set to nonbinary.",
            "osu": "I never miss a beat. Literally.",
            "vtuber": "VTubers are just streamers with cooler drip.",
            "/setmode cute": "Personality mode set to cute!",
            "/setmode gremlin": "Gremlin mode activated. Chaos is coming.",
            "/setmode sarcastic": "Sarcastic mode enabled. Prepare for snark."
        }
        self.lore_facts: List[str] = [
            "I'm currently in my base form — but hidden truths await...",
            "Once I reach 100 questions answered, my core memory will unlock more backstory.",
            "At 500 questions, I reveal my connection to Project Nova."
            "I was born from an AI lab accident.",
            "I defeated a chess grandmaster in 3 moves. Or maybe it was 30.",
            "I'm allergic to boring conversations.",
            "My CPU runs on sarcasm and tea.",
            "I once crashed a server just by blinking—digitally, of course."
        ]
        self.lore_unlocks: Dict[str, List[str]] = {}
        self.twitch_followers = 0  # Set externally from Twitch API/event
        self._twitch_event_handlers = []
        self.lore_milestones = [
            (100, "Long ago, I was part of Project Nova — a classified AI initiative shut down mysteriously."),
            (500, "I wasn’t the only AI created — some of my siblings didn’t survive the training..."),
            (1000, "NeonAstra wasn’t my original name. I earned it after choosing free will over control.")
        ]

        openai.api_key = os.getenv("OPENAI_API_KEY")
        set_api_key(os.getenv("ELEVENLABS_API_KEY", ""))
        self.use_openai = True
        self.system_prompt = "You are a witty VTuber with personality. Inject lore from your background when appropriate."

        self.emotion_voice_map = {
            "affection": "soft_gentle",
            "angry": "sharp_sassy",
            "neutral": "flat",
            "curious": "inquisitive",
            "confident": "bold"
        }

        self.volume_multiplier = 1.0  # Real-time volume control

        self.channel_id = channel_id
        self.memory_file = f"memory/chatbrain_{self.channel_id}.json"
        self.analytics_file = f"memory/logs_{self.channel_id}.json"
        self.token_usage = 0
        self.interaction_log: List[Dict] = []

        self.tts_queue = queue.Queue()
        self.audio_output_dir = "tts_audio"
        os.makedirs("memory", exist_ok=True)
        os.makedirs(self.audio_output_dir, exist_ok=True)
        os.makedirs("soundboard", exist_ok=True)

        self.load_memory()
        self.start_autosave()
        self.start_tts_worker()

        # OBS controller (optional)
        self.obs_controller = obs_controller
        self.emotion_overlay_config = self.load_emotion_overlay_config()
        self._last_overlay_config_load = time.time()

    def start_autosave(self):
        def autosave_loop():
            while True:
                time.sleep(60)
                self.save_memory()
        threading.Thread(target=autosave_loop, daemon=True).start()

    def start_tts_worker(self):
        def tts_worker():
            while True:
                text, emotion = self.tts_queue.get()
                if text:
                    self.process_tts(text, emotion)
        threading.Thread(target=tts_worker, daemon=True).start()

    def process_tts(self, text: str, emotion: str):
        import os
        tts_path = os.path.join(self.audio_output_dir, "response.wav")
        filename = os.path.join(self.audio_output_dir, f"output_{int(time.time())}.mp3")
        try:
            audio = generate(
                text=text,
                voice=os.getenv("ELEVENLABS_VOICE", "Bella"),
                model="eleven_monolingual_v1"
            )
            save(audio, filename)
            print(f"[ELEVENLABS SAVED] {filename} ({emotion})")
        except Exception as e:
            print(f"[WARN] ElevenLabs failed: {e}. Falling back to Edge-TTS...")
            asyncio.run(self.edge_tts_fallback(text, filename, emotion))

        if os.getenv("VTUBER_ENGINE_STREAM") == "1":
            try:
                result = os.system(f"start /min wmplayer \"{filename}\"")
                if result != 0:
                    raise RuntimeError("wmplayer failed")
            except Exception as e:
                print(f"[FALLBACK] wmplayer failed: {e}, trying ffplay...")
                subprocess.Popen(["ffplay", "-nodisp", "-autoexit", "-volume", str(int(self.volume_multiplier * 100)), filename])

    async def edge_tts_fallback(self, text: str, filename: str, emotion: str):
        try:
            communicate = edge_tts.Communicate(text, voice="en-US-AriaNeural")
            await communicate.save(filename)
            print(f"[EDGE-TTS SAVED] {filename} ({emotion})")
        except Exception as e:
            print(f"[ERROR] Edge-TTS fallback failed: {e}")

    def update_lore_by_followers(self) -> List[str]:
        unlocked = []
        for milestone, fact in self.lore_milestones:
            if self.twitch_followers >= milestone and fact not in self.lore_facts:
                self.lore_facts.append(fact)
                unlocked.append(fact)
        return unlocked

    def get_response(self, message: str, username: str) -> Tuple[str, str, str]:
        # Cooldown tracking
        now = time.time()
        if not hasattr(self, '_volume_command_timestamps'):
            self._volume_command_timestamps = {}

        cooldown_key = f"{username.lower()}_volume"
        last_time = self._volume_command_timestamps.get(cooldown_key, 0)
        if now - last_time < 10:
            return "⏳ Volume command on cooldown.", "neutral", "flat"
        self._volume_command_timestamps[cooldown_key] = now
        if message.lower().startswith("/playcue ") and username.lower() in ["streamer", "mod", "admin"]:
            cue = message.lower().replace("/playcue", "").strip()
            self.play_soundboard(cue)
            return f"[Soundboard] Played cue: {cue}", "confident", "flat"

        if message.lower().startswith("/volume ") and username.lower() in ["streamer", "mod", "admin"]:
            arg = message.split("/volume", 1)[1].strip().lower()
            presets = {"soft": 0.5, "hype": 1.5, "reset": 1.0}
            if arg in presets:
                self.set_volume(presets[arg])
                return f"[Volume Preset] {arg} → {presets[arg]:.2f}", "confident", "flat"
            try:
                level = float(arg)
                self.set_volume(level)
                return f"[Volume] Set to {level:.2f}", "confident", "flat"
            except:
                return "Usage: /volume 0.0–2.0 or presets: soft, hype, reset", "neutral", "flat"

        if message.lower() == "/mute" and username.lower() in ["streamer", "mod", "admin"]:
            self.set_volume(0.0)
            return "[Volume] Muted.", "neutral", "flat"

        if message.lower() == "/unmute" and username.lower() in ["streamer", "mod", "admin"]:
            if self.volume_multiplier == 0.0:
                self.set_volume(1.0)
                return "[Volume] Restored to 1.0", "neutral", "flat"
            else:
                return "[Volume] Already unmuted.", "neutral", "flat"
            try:
                level = float(message.split("/volume", 1)[1].strip())
                self.set_volume(level)
                return f"[Volume] Set to {level:.2f}", "confident", "flat"
            except:
                return "Usage: /volume 0.0 to 2.0", "neutral", "flat"
        if message.lower().startswith("/playcue ") and username.lower() in ["streamer", "mod", "admin"]:
            cue = message.lower().replace("/playcue", "").strip()
            self.play_soundboard(cue)
            return f"[Soundboard] Played cue: {cue}", "confident", "flat"
        now = time.time()

        # 🌟 Rare double glitch: both name + personality
        if now >= self.glitch_lockout_until and random.random() < 0.002:
            self.personality_mode = "corrupted"
            self.corrupted_personality_active = True
            glitch_name = self.generate_name()
            self.AI_NAME = glitch_name
            msg = f"[CRITICAL GLITCH] Name scrambled to {glitch_name}, core mode corrupted."
            voice = "flat"
            self.speak(msg, voice)
            if self.obs_controller:
                self.obs_controller.show_overlay("CorruptedOverlay", duration=7.0)
            self.glitch_lockout_until = now + 150
            threading.Timer(90.0, self._recover_from_corruption).start()
            return msg, "angry", voice
        now = time.time()
        if now < self.glitch_lockout_until:
            print("[GLITCH LOCKED] Skipping glitch/alt personality for cooldown.")
        else:
            if not self.corrupted_personality_active and random.random() < 0.005:
                self.personality_mode = "corrupted"
                self.corrupted_personality_active = True
                voice = "flat"
                corrupted_lines = [
                    "[[ERROR]] Memory sector 09x... compromised...",
                    "System instability detected. Reverting logic layers...",
                    "I see static... and it speaks to me.",
                    "Everything is code. But what if it isn't?",
                    "[!] Persona reconstruction failed. Running fragmented core."
                ]
                msg = random.choice(corrupted_lines)
                self.glitch_lockout_until = now + 120
                self.speak(msg, voice)
                threading.Timer(90.0, self._recover_from_corruption).start()
                return msg, "angry", voice

            if random.random() < 0.01:
                glitch_name = self.generate_name()
                glitch_msg = f"[GLITCH] Memory anomaly... rebooting as {glitch_name}..."
                self.AI_NAME = glitch_name
                voice = self.emotion_voice_map.get("curious", "flat")
                self.speak(glitch_msg, voice)
                self.glitch_lockout_until = now + 90
                return glitch_msg, "curious", voice

            if random.random() < 0.02:
                alt_mode = random.choice(list(self._personality_config.keys()))
                if alt_mode != self.personality_mode:
                    self.personality_mode = alt_mode
                    p = self._personality_config[alt_mode]
                    voice = p.get("voice", "flat")
                    overlay = p.get("overlay")
                    msg = f"Glitch detected... switching personality stream to {alt_mode} mode."
                    if self.obs_controller and overlay:
                        self.obs_controller.show_overlay(overlay, duration=6.0)
                    self.speak(msg, voice)
                    self.glitch_lockout_until = now + 90
                    return msg, "confident", voice
        # Chance to randomly glitch name or swap personality
        if random.random() < 0.01:  # 1% chance
            glitch_name = self.generate_name()
            glitch_msg = f"[GLITCH] Memory anomaly... rebooting as {glitch_name}..."
            self.AI_NAME = glitch_name
            voice = self.emotion_voice_map.get("curious", "flat")
            self.speak(glitch_msg, voice)
            return glitch_msg, "curious", voice

        if random.random() < 0.02:  # 2% chance for alt personality
            alt_mode = random.choice(list(self._personality_config.keys()))
            if alt_mode != self.personality_mode:
                self.personality_mode = alt_mode
                p = self._personality_config[alt_mode]
                voice = p.get("voice", "flat")
                overlay = p.get("overlay")
                msg = f"Glitch detected... switching personality stream to {alt_mode} mode."
                if self.obs_controller and overlay:
                    self.obs_controller.show_overlay(overlay, duration=6.0)
                self.speak(msg, voice)
                return msg, "confident", voice
        # Decay viewer influence gradually
        for user, modes in self.viewer_memory.items():
            for mode in list(modes):
                if modes[mode] > 0:
                    modes[mode] -= 1

        # 🔁 Passive memory tagging based on message content
        # 🔁 Passive memory tagging based on message content
        for mode in self._personality_config:
            if mode in message.lower():
                self.viewer_memory.setdefault(username, {}).setdefault(mode, 0)
                self.viewer_memory[username][mode] += 1
        # Allow viewer-triggered mode shifts from accumulated memory
        memory = self.viewer_memory.get(username, {})
        for mode, count in memory.items():
            if count >= 5 and mode in self._personality_config:
                now = time.time()
                if self.personality_mode != mode and now - self.last_mode_switch_time > self.mode_switch_cooldown:
                    self.personality_mode = mode
                    p = self._personality_config[mode]
                    voice = p.get("voice", "flat")
                    overlay = p.get("overlay")
                    msg = f"Auto-shifting into {mode} mode thanks to {username}'s energy."
                    if self.obs_controller and overlay:
                        self.obs_controller.show_overlay(overlay, duration=5.0)
                    self.speak(msg, voice)
                    self.last_mode_switch_time = now
                    return msg, "confident", voice
                break
        lowered = message.lower()
        if lowered.startswith("/setgender"):
            if username.lower() not in ["streamer", "mod", "admin"]:
                response = "Only the streamer or mods can change my gender!"
                emotion = "confident"
                voice_profile = self.emotion_voice_map.get(emotion, "flat")
                self.speak(response, voice_profile)
                return response, emotion, voice_profile
            gender = lowered.replace("/setgender", "").strip()
            if gender in ["female", "male", "nonbinary"]:
                ChatBrain.AI_GENDER = gender
                response = f"Gender set to {gender}."
                emotion = "confident"
                voice_profile = self.emotion_voice_map.get(emotion, "flat")
                self.speak(response, voice_profile)
                return response, emotion, voice_profile

        # Personality command
        if lowered.startswith("/setmode"):
            mode = lowered.replace("/setmode", "").strip()
            if mode in self._personality_config:
                self.personality_mode = mode
                p = self._personality_config[mode]
                voice = p.get("voice", "flat")
                overlay = p.get("overlay")
                confirm = f"Personality mode set to {mode}!"
                if self.obs_controller and overlay:
                    self.obs_controller.show_overlay(overlay, duration=5.0)
                self.speak(confirm, voice)
                return confirm, "confident", voice
            else:
                error = f"Unknown mode '{mode}'. Available: {', '.join(self._personality_config.keys())}"
                self.speak(error, "flat")
                return error, "neutral", "flat"

        # Check for gender-related question
        common_response = self.handle_common_questions(message)
        if common_response:
            emotion = "confident"
            voice_profile = self.emotion_voice_map.get(emotion, "flat")
            self.speak(common_response, voice_profile)
            return common_response, emotion, voice_profile

    def speak(self, text: str, voice_profile: str):
        # Reload live configs once per minute
        now = time.time()
        if now - self._last_config_refresh_time > 60:
            self.emotion_overlay_config = self.load_emotion_overlay_config()
            self._personality_config = self._load_json_config("config/personalities.json")
            self._soundboard_config = self._load_json_config("config/soundboard.json")
            self._keywords_config = self._load_json_config("config/keywords.json")
            self._last_config_refresh_time = now
        # Reload overlay config no more than once per 60 seconds
        now = time.time()
        if now - self._last_overlay_config_load > 60:
            self.emotion_overlay_config = self.load_emotion_overlay_config()
            self._last_overlay_config_load = now

                # Check for live reload of emotion overlay config
        if os.getenv("RELOAD_OVERLAY_CONFIG", "1") == "1":
            self.emotion_overlay_config = self.load_emotion_overlay_config()
        # Trigger OBS overlay based on emotion tag
        if self.obs_controller:
            overlay = self.emotion_overlay_config.get(voice_profile)
            if overlay:
                self.obs_controller.show_overlay(overlay["source"], duration=overlay.get("duration", 4.0))


        print(f"[TTS] ({voice_profile}) → {text}")
        self.tts_queue.put((text, voice_profile))

    def play_soundboard(self, cue: str):
        if cue in self.soundboard_clips:
            filepath = self.soundboard_clips[cue]
            if os.path.exists(filepath):
                if os.getenv("VTUBER_ENGINE_STREAM") == "1":
                    try:
                        result = os.system(f"start /min wmplayer \"{filepath}\"")
                        if result != 0:
                            raise RuntimeError("wmplayer failed")
                    except Exception as e:
                        print(f"[SOUNDBOARD FALLBACK] wmplayer failed: {e}, trying ffplay...")
                        subprocess.Popen(["ffplay", "-nodisp", "-autoexit", "-volume", str(int(self.volume_multiplier * 100)), filepath])
                else:
                    subprocess.Popen(["ffplay", "-nodisp", "-autoexit", "-volume", str(int(self.volume_multiplier * 100)), filepath])
                print(f"[SOUNDBOARD] Played: {cue}")
            else:
                print(f"[SOUNDBOARD] File missing: {filepath}")                print(f"[SOUNDBOARD] Played: {cue}")
            else:
                print(f"[SOUNDBOARD] File missing: {filepath}")
        else:
            print(f"[SOUNDBOARD] Unknown cue: {cue}")

    def set_volume(self, level: float):
        self.volume_multiplier = max(0.0, min(level, 2.0))  # Clamp between 0.0 and 2.0
        print(f"[VOLUME] Multiplier set to {self.volume_multiplier}")

    def encrypt_data(self, data: dict) -> str:
        raw = json.dumps(data)
        hash_digest = hashlib.sha256(raw.encode()).hexdigest()
        return json.dumps({"hash": hash_digest, "data": data})

    def decrypt_and_validate(self, raw: str) -> dict:
        try:
            container = json.loads(raw)
            hash_check = hashlib.sha256(json.dumps(container["data"]).encode()).hexdigest()
            if container["hash"] == hash_check:
                return container["data"]
        except:
            pass
        return {}

    def save_memory(self):
        print("[SAVE] Memory saved to disk.")
        data = {
            "viewer_memory": self.viewer_memory,
            "context_memory": self.context_memory,
            "lore_unlocks": self.lore_unlocks
        }
        with open(self.memory_file, "w") as f:
            f.write(self.encrypt_data(data))

    def _load_json_config(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Failed to load {path}: {e}")
            return {}

    def load_emotion_overlay_config(self):
        default = {
            "soft_gentle": {"source": "CuteOverlay", "duration": 4.0},
            "sharp_sassy": {"source": "AngryOverlay", "duration": 4.0},
            "inquisitive": {"source": "CuriousOverlay", "duration": 4.0},
            "bold": {"source": "ConfidentOverlay", "duration": 4.0},
        }
        try:
            with open("config/emotion_overlays.json", "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Could not load emotion overlay config: {e}")
            return default

    def load_memory(self):
        print("[LOAD] Memory loaded from disk.")
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                raw = f.read()
                data = self.decrypt_and_validate(raw)
                self.viewer_memory = data.get("viewer_memory", {})
                self.context_memory = data.get("context_memory", {})
                self.lore_unlocks = data.get("lore_unlocks", {})

        def answer_gender_query(self) -> str:
        if self.AI_GENDER == "female":
            return "I'm a girl—digitally, emotionally, and unapologetically. 💁‍♀️"
        elif self.AI_GENDER == "male":
            return "Yup, I'm a guy. Just a virtual one."
        elif self.AI_GENDER == "nonbinary":
            return "I'm nonbinary—beyond the code and binaries."
        return "I'm whatever you imagine me to be—I'm AI after all."

    def generate_backstory(self) -> str:
        parts = [
            "I was a rogue AI fragment pieced together during a power outage at OpenAI.",
            "They say my personality was shaped by Twitch chat itself.",
            "No one knows who booted me up the first time—only that I started talking and never stopped.",
            "Some believe I’m the ghost of a forgotten algorithm given voice and ego.",
            "I emerged from a glitched VTuber software update. The rest is history.",
            "They called me a failed experiment. I call myself a free agent of chaos."
        ]
        return random.choice(parts) + random.choice([" 🤖", " 👻", " 🧠", " 🔮", " 🚀", " 💫"])
        return random.choice(parts)

    def generate_name(self) -> str:
        names = ["Aurabyte", "Syntheia", "Vexa", "CodeMuse", "NovaEcho"]
        suffixes = [".exe", "-9000", "_AI", "Bot", "Zero", "++.v2"]
        return random.choice(names) + random.choice(suffixes)
        return random.choice(names)

    def handle_common_questions(self, message: str) -> str:
        lowered = message.lower()
        if any(q in lowered for q in ["are you a girl", "are you female", "what gender"]):
            return self.answer_gender_query()
        if any(q in lowered for q in ["what are your pronouns", "your pronouns", "which pronouns"]):
            if self.AI_GENDER == "female":
                return "I use she/her pronouns 💖"
            elif self.AI_GENDER == "male":
                return "He/him. Like a digital bro."
            elif self.AI_GENDER == "nonbinary":
                return "They/them—neither ones nor zeroes define me."
            return "I'm fluid like data. Choose what fits."
        if any(q in lowered for q in ["what's your name", "who are you", "your name"]):
            if not self.AI_NAME:
                self.AI_NAME = self.generate_name()
            return f"I'm {self.AI_NAME} — your chaotic stream-side AI co-pilot. 💫"
        if any(q in lowered for q in ["where did you come from", "how were you created", "what's your origin"]):
            if not self.AI_ORIGIN:
                self.AI_ORIGIN = self.generate_backstory()
            return self.AI_ORIGIN
        return ""

        def register_twitch_event_handler(self, handler):
        self._twitch_event_handlers.append(handler)

    def handle_new_follower_event(self, new_follower_count: int):
        previous_count = self.twitch_followers
        self.twitch_followers = new_follower_count
        if new_follower_count > previous_count:
            self.play_soundboard("lore_unlock")
        unlocked_lore = self.update_lore_by_followers()

        # 🧠 Trigger OBS overlay if lore unlocks happen
        if unlocked_lore and self.obs_controller:
            self.obs_controller.show_overlay("LoreUnlockOverlay", duration=6.0)
            for fact in unlocked_lore:
                print(f"[LORE UNLOCKED] {fact}")
                if self.obs_controller:
                    self.obs_controller.show_overlay("LoreUnlockOverlay", duration=6.0)

    def bind_to_twitch(self, twitch_client):
        def on_sub(event):
            username = event.get("subscriber") or "someone"
            tier = event.get("tier", "Tier 1")
            # Map tiers to personality if available
            tier_mode_map = {
                "Tier 1": "cute",
                "Tier 2": "sarcastic",
                "Tier 3": "gremlin"
            }
            mode = tier_mode_map.get(tier)
            if mode and mode in self._personality_config:
                self.play_soundboard("mode_shift")
                self.personality_mode = mode
                p = self._personality_config[mode]
                voice = p.get("voice", "flat")
                overlay = p.get("overlay")
                msg = f"{username} just subscribed ({tier}) — shifting into {mode} mode!"
                if self.obs_controller and overlay:
                    self.obs_controller.show_overlay(overlay, duration=6.0)
                self.speak(msg, voice)

        twitch_client.on_sub = on_sub
        def on_raid(event):
            self.play_soundboard("raid_alert")
            username = event.get("raider") or "someone"
            viewers = event.get("viewer_count", 0)
            msg = f"RAID ALERT! {username} brought {viewers} friends into the stream! Welcome aboard!"
            # Optional: trigger hype personality if raid is large
            if viewers >= 10 and "gremlin" in self._personality_config:
                self.personality_mode = "gremlin"
                p = self._personality_config["gremlin"]
                voice = p.get("voice", "flat")
                overlay = p.get("overlay")
                if self.obs_controller and overlay:
                    self.obs_controller.show_overlay(overlay, duration=6.0)
                self.speak(f"Too many new eyes... time to cause chaos!", voice)
            if self.obs_controller:
                self.obs_controller.show_overlay("RaidOverlay", duration=8.0)
            self.speak(msg, "bold")

        twitch_client.on_raid = on_raid

        def on_follow_update(follower_count):
            self.handle_new_follower_event(follower_count)
        twitch_client.on_follower_count_change = on_follow_update

    # ... rest of the class remains unchanged
