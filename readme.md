---

## ✅ Core Feature Overview

### 🎙️ Voice & Emotion Recognition

**Path:** `modules/voice/`

- Uses Whisper to detect tone, speaker identity
- Emotion classification feeds into memory, voice modulation
- Discord listener supports multi-speaker memory tagging

### 🎭 Personality & Mode Switching

**Path:** `modules/persona/`

- Supports `/setmode` commands
- Linked to TTS, visual, and behavioral modes
- Viewers influence persona shifts with cooldowns

### 🧠 Memory Engine (Persistent)

**Path:** `memory/`, `modules/memory/`

- JSON file per channel/server, encrypted
- Autosaves, version upgrades supported
- Tracks mood, interactions, emotion score per user

### 💬 ChatBrain + LLM Integration

**Path:** `core/chatbrain.py`

- Injects memory, emotion, lore into GPT/local LLM
- Auto-alters response tone based on emotional history
- Glitched dialogue injection from corruption engine

### 📺 OBS / VTube Studio Integration

**Path:** `modules/obs/`, `modules/vts/`

- WebSocket overlay effect triggers
- Auto-expression and scene based on emotion
- Glitch effects + transitions

### 🎶 AI Singing System

**Path:** `modules/singing/`

- Melody learning from YT clips
- Emotion-based tone matching and lyric recall
- Visual lyric bounce sync in progress

### 🔊 TTS + Audio Engine

**Path:** `modules/tts/`

- ElevenLabs (primary), Edge-TTS (backup), VoiceAI
- Emotion → voice style, pitch, rate
- .mp3 export for stream re-use, live queue playback

### 📋 GUI Control Dashboard (React)

**Path:** `gui/`

- Mood toggles, corruption decay, trigger injects
- Terminal UI aesthetic, auto-refresh log toggles

---

## 🧬 Memory Corruption Engine

**Path:** `modules/corruption/`

- Persona and response corruption logic
- Triggered on emotion overload or milestone
- Auto-decay and mod-triggered restore
- Voice + overlay glitch effects

---

## 🧪 Optional & Experimental Modules

| Module              | Description                               |
| ------------------- | ----------------------------------------- |
| Lore Timeline GUI   | Visual tracker for unlocks & arcs         |
| Remote Auth         | Mod verification via Twitch/YouTube login |
| Prompt Analytics    | Logs token usage, viewer influence tags   |
| Stream Cluster Sync | Multi-instance streamer support           |
| Singing Overlay     | Auto-lyric bounce synced with emotion     |
| Persona Matching    | Persona inference from viewer style       |

---

## 📁 Suggested Project Structure

```bash
├── core/
│   └── chatbrain.py
├── modules/
│   ├── voice/
│   ├── memory/
│   ├── persona/
│   ├── tts/
│   ├── singing/
│   ├── obs/
│   ├── vts/
│   └── corruption/
├── auth/
│   └── remote_auth_server.py
├── gui/
│   ├── CorruptionDecayPanel.jsx
│   └── GlitchLogControlPanel.jsx
├── tools/
│   ├── RemoteControlTerminalUI.py
│   ├── launch_auth_server.bat
│   └── launch_remote_control.bat
├── memory/
│   └── *.json
```

---

## 📦 Remote Tools

- `launch_auth_server.bat` → Twitch/YT mod validation
- `launch_remote_control.bat` → Remote terminal UI trigger interface
- `requirements.txt`

---

## 💻 Requirements

- Python 3.9+
- Node.js + React
- Discord.py, Whisper, OBS WebSocket, ElevenLabs API

---

## 🧠 Dev Snippet

```py
chatbrain_instances[guild_id] = ChatBrain(channel_id=f"discord_{guild_id}")
```

---

## 📥 Downloadable README

This file is ready to export as `README.md` for your GitHub project.

> This README will continue to evolve as more modules are added. Be sure to sync whenever new core systems are implemented.

