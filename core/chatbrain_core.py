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
from flask import Flask, request, jsonify  # 🌐 Remote control API
from obs_websocket_service import OBSController  # 🧠 OBS integration

app = Flask(__name__)  # remote API app instance

class ChatBrain:
    def __init__(self):
        self.start_corruption_decay()
        self.start_remote_control_api()

    def start_remote_control_api(self):
        chatbrain = self  # reference for inner routes

        @app.route("/api/status")
        def status():
            return jsonify({
                "corruption_level": chatbrain.get_corruption_level(),
                "persona": chatbrain.get_active_persona()
            })

        @app.route("/api/logs/glitch")
        def glitch_log():
            return jsonify(chatbrain.get_glitch_log_ui())

        @app.route("/api/control/trigger", methods=["POST"])
        def trigger_corruption():
            data = request.json
            result = chatbrain.force_glitch_response(data.get("level", 50))
            return jsonify({"result": result})

        @app.route("/api/control/restore", methods=["POST"])
        def restore():
            try:
                corruption_path = "memory/memory_integrity.json"
                if os.path.exists(corruption_path):
                    with open(corruption_path, "r") as f:
                        memory = json.load(f)
                    memory["corruption_level"] = 0
                    with open(corruption_path, "w") as f:
                        json.dump(memory, f, indent=2)
                return jsonify({"restored": True})
            except Exception as e:
                return jsonify({"error": str(e)})

        threading.Thread(target=lambda: app.run(host="0.0.0.0", port=6543), daemon=True).start()

    def get_corruption_level(self):
        try:
            with open("memory/memory_integrity.json", "r") as f:
                data = json.load(f)
            return data.get("corruption_level", 0)
        except:
            return 0

    def get_active_persona(self):
        try:
            with open("memory/corruption_persona.json", "r") as f:
                persona = json.load(f)
            return persona.get("name", "Default")
        except:
            return "Default"

    def force_glitch_response(self, level):
        try:
            corruption_path = "memory/memory_integrity.json"
            if os.path.exists(corruption_path):
                with open(corruption_path, "r") as f:
                    data = json.load(f)
            else:
                data = {}
            data["corruption_level"] = min(100, max(0, level))
            with open(corruption_path, "w") as f:
                json.dump(data, f, indent=2)
            return f"Corruption level forced to {level}"
        except Exception as e:
            return f"[ERROR] Could not force corruption level: {e}"

    # ... rest of existing methods remain unchanged ...
