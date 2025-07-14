# 🧠 Discord Voice Listener Bot for AI VTuber

This is a persistent, multi-speaker-enabled Discord voice listener designed to power a reactive AI VTuber — supporting full emotion-aware speech recognition, OBS + VTube Studio reaction control, lore integration, personality switching, and more.

---

## ✅ Features Implemented

### 🔊 Real-Time Voice Capture

- Listens to Discord voice channels with Whisper AI
- Identifies individual speakers with per-user memory
- Emotion estimation from speech tone (volume-based fallback)

### 🎭 Dynamic Personality System

- `/setmode <persona>` command toggles VTuber mode live
- Auto-loads recovery phrases, tone, and expressions
- Visual + narration confirmation (via VTS + TTS)

### 📺 OBS & VTube Studio Integration

- OBS scene switches based on AI-detected emotions (e.g., glitch → Scene\_Glitch)
- VTS expression changes via WebSocket hotkeys (e.g., blush, angry, neutral)
- Auto-revert system (resets scene + expression after emotion decay)

### 🧠 ChatBrain + LLM Hook

- Emotion-labeled responses generated via ChatBrain (GPT/local LLM)
- Per-speaker emotional influence mapping
- Lore event triggers + context-aware replies

### 🗂️ Persona-Aware Config

- `settings.json` includes:
  - persona-specific recovery voice lines
  - VTS hotkey expression triggers
  - OBS scene maps per emotion
- Persona state persisted per server/guild

### 💾 Memory & Logging

- Per-user voice memory cache (`voice_speaker_cache.json`)
- Emotion decay timers (`decay_*.json`) with auto-reset
- All voice events & reverts logged in `logs/voicebot.log`

### 🛠️ Error Handling & Fallback

- If TTS fails, fallback prints to console + SFX
- VTS and OBS errors caught with minimal impact
- Custom emotion tone styles per speech intensity (e.g., whispery → pitch+rate)

---

## 📁 Folder Structure

```
├── config/
│   └── settings.json       # OBS/VTS hotkeys, persona data
│   └── voice_styles.json   # Optional custom pitch/rate/style per tone
├── memory/
│   └── voice_speaker_cache_<guild>.json
│   └── decay_<guild>.json
│   └── persona_mode_<guild>.json
├── soundboard/
│   └── revert_sfx.mp3
│   └── tts_fallback.mp3
├── logs/
│   └── voicebot.log
```

---

## 🔧 Requirements

- Python 3.9+
- `discord.py`, `speechrecognition`, `websockets`, `obswebsocket`, `whisper`, `ffmpeg`, `ChatBrain`
- OBS WebSocket v5+ installed + configured
- VTube Studio with WebSocket plugin enabled

---

## 🧪 Roadmap / Optional Add-ons

- 🎙️ YouTube relay listener (YT → Discord text → ChatBrain)
- 🧩 Voice activity detection to improve speaker ID
- 🧬 Dynamic lore-based expression blending
- 💬 Twitch chat relay → emotional triggers (milestones, redeems)
- 🎛️ Web dashboard for real-time control (mode switches, emotion force)
- 🔒 Mod-access toggles to restrict reactions/live voice

---

## 🧠 Maintainer Notes

This bot is part of the **Ai VTuber Core Stack**, designed to mirror and expand on what Neuro-sama and other real-time AI avatars do, with extensible memory, emotion, and voice layering.

For full integration, wire into the `ChatBrain` instance with:

```python
chatbrain_instances[guild_id] = ChatBrain(channel_id=f"discord_{guild_id}")
```

---

## 🧵 Contact / Support

Need help wiring into OBS or syncing VTS expressions? Just ask!

