# .gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.env
*.env
memory/
tts_audio/
soundboard/
*.log

# README.md
# Chatbrain-VTuber

An advanced AI VTuber core engine with emotional intelligence, TTS, glitch mechanics, Twitch integration, and dynamic lore.

## 🚀 Features
- GPT / Local LLM integration
- ElevenLabs & Edge-TTS fallback
- OBS & VTube Studio overlay control
- Memory, viewer tagging, emotional response
- Glitch personalities and recovery system

## 🛠️ Install
```bash
pip install .
```

## 🧠 Run
```bash
chatbrain-run
```

## ⚙️ Dev Setup
```bash
git clone https://github.com/yourname/chatbrain-vtuber.git
cd chatbrain-vtuber
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🔧 Environment
Set these in `.env`:
```
OPENAI_API_KEY=yourkey
ELEVENLABS_API_KEY=yourkey
VTUBER_ENGINE_STREAM=1
```

## 📡 Twitch Integration
Hook into Twitch using the provided `bind_to_twitch()` method.

---
Built with ❤️ for immersive VTuber streaming.
