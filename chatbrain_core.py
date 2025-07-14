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
import yt_dlp  # 🎵 YouTube source learning
import librosa  # 🎵 Pitch and phoneme alignment

from obs_websocket_service import OBSController  # 🧠 OBS integration

class ChatBrain:
    def process_singing_sources(self):
        """
        Auto-loads sing_profile.json and runs learning on unprocessed sources.
        """
        try:
            with open("memory/sing_profile.json", "r") as f:
                profile = json.load(f)
                sources = profile.get("learning_sources", [])
                updated = False
                count = 0
                for src in sources:
                    if not src.get("learned", False):
                        self.learn_singing_from_source(src["type"], src)
                        src["learned"] = True
                        updated = True
                        count += 1
                if updated:
                    print(f"[🎵 LEARNED] {count} new singing source(s) processed.")
                    with open("memory/sing_profile.json", "w") as f2:
                        json.dump(profile, f2, indent=2)
        except Exception as e:
            print(f"[ERROR] Failed to process singing sources: {e}")

    def learn_singing_from_source(self, source_type: str, source_info: dict):
        import random
        import time
        profile_path = "memory/sing_profile.json"
        try:
            audio_path = None
            if source_type == "youtube":
                url = source_info.get("url")
                if url:
                    print(f"[YOUTUBE] Downloading {url}...")
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': 'temp/sing_input.%(ext)s',
                        'quiet': True,
                        'noplaylist': True,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'wav',
                            'preferredquality': '192',
                        }]
                    }
                    os.makedirs("temp", exist_ok=True)
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    audio_path = "temp/sing_input.wav"
            elif source_type == "file":
                audio_path = source_info.get("path")

            pitch_curve, tempo = self.analyze_pitch_and_tempo(audio_path)

            with open(profile_path, "r") as f:
                profile = json.load(f)

            melody_id = f"melody_{int(time.time())}_{random.randint(1000, 9999)}"
            profile.setdefault("melody_profiles", {})[melody_id] = {
                "source": source_info,
                "emotion_hint": "confident",
                "tempo": tempo,
                "pitch_curve": pitch_curve,
                "lyric_map": ["la", "la", "da", "dee", "la", "na", "ha", "woo"]
            }

            with open(profile_path, "w") as f:
                json.dump(profile, f, indent=2)

            print(f"[🎵 SAVED] New melody profile added: {melody_id}")

            # 🔊 Auto-generate audio preview
            preview_path = f"memory/audio/{melody_id}.mp3"
            try:
                os.makedirs("memory/audio", exist_ok=True)
                text = " ".join(profile["melody_profiles"][melody_id]["lyric_map"])
                emotion = profile["melody_profiles"][melody_id]["emotion_hint"]
                tts = gTTS(text=text, lang='en')
                tts.save(preview_path)
                print(f"[🔊 AUDIO] Preview saved to {preview_path}")
            except Exception as audio_error:
                print(f"[AUDIO ERROR] Failed to save preview: {audio_error}")

        except Exception as e:
            print(f"[ERROR] Failed to save melody: {e}")

    def analyze_pitch_and_tempo(self, filepath: str):
        try:
            print(f"[ANALYSIS] Extracting pitch from {filepath}")
            y, sr = librosa.load(filepath)
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            tempo = int(librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0])
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            mean_pitches = [int(p.max()) for p in pitches.T[::len(pitches.T)//16] if p.max() > 0]
            return mean_pitches or [65] * 16, tempo
        except Exception as e:
            print(f"[ERROR] Pitch extraction failed: {e}")
            return [65] * 16, 100

    # 🎵 (rest of the class remains unchanged)

    def handle_incoming_chat(self, message: str, username: str, platform: str = "twitch"):
        if message.lower().startswith("/previewmelody "):
            melody_id = message.split("/previewmelody", 1)[1].strip()
            preview_path = f"memory/audio/{melody_id}.mp3"
            if os.path.exists(preview_path):
                try:
                    print(f"[🔊 PLAYBACK] Previewing {melody_id}")
                    os.system(f'start /min wmplayer "{preview_path}"')
                    return f"🎧 Playing preview for {melody_id}", "confident", "flat"
                except Exception as e:
                    return f"[ERROR] Failed to preview: {e}", "angry", "flat"
            else:
                return f"No preview audio found for {melody_id}", "neutral", "flat"
        if message.lower().startswith("/learnsing "):
            url = message.split("/learnsing", 1)[1].strip()
            if "youtube.com" in url or "youtu.be" in url:
                print(f"[🎹 CHAT COMMAND] Learning song from: {url}")
                try:
                    with open("memory/sing_profile.json", "r") as f:
                        profile = json.load(f)
                    profile.setdefault("learning_sources", []).append({
                        "type": "youtube",
                        "url": url,
                        "learned": False
                    })
                    with open("memory/sing_profile.json", "w") as f:
                        json.dump(profile, f, indent=2)
                    self.process_singing_sources()
                    return f"🎶 Learned new melody from YouTube!", "confident", "flat"
                except Exception as e:
                    return f"[ERROR] Failed to learn song: {e}", "angry", "flat"
        elif message.lower().startswith("/singstatus"):
            try:
                with open("memory/sing_profile.json", "r") as f:
                    profile = json.load(f)
                total = len(profile.get("melody_profiles", {}))
                return f"🎼 Melody profiles stored: {total}", "neutral", "flat"
            except:
                return "No melody profile data found.", "neutral", "flat"
