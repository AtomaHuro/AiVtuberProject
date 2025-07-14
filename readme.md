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

- On Twitch sub/follow/raid, triggers milestone scan from `lore_events.json`

- Plays mapped voice line from `lore_voice.json` (pitch, style, tone)

- Optional scene or expression override using VTS/OBS

- Integrates with `lore_events.json` to detect and respond to milestone triggers

- Twitch event listener updates emotional state and timeline milestones

- Memory unlocks tied to subscriber/follower/raid counts

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

### 🔒 Secure, Validated Memory System

- Memory JSON files are encryption-ready

- Prevents memory loss or corruption from crashes

- Supports future version-based memory schema upgrades

- Modular design allows for safe memory migrations

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
├── memory/
│   └── lore_voice.json       # Voice line mapping per lore event
```

```
├── memory/
│   └── lore_events.json      # Timeline triggers and milestone states
```

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

- Optional adaptive performance tuning

  - Limits processing intensity to prevent CPU/GPU overload
  - Graceful fallback to simpler TTS or expression flows on weak hardware

- Python 3.9+

- `discord.py`, `speechrecognition`, `websockets`, `obswebsocket`, `whisper`, `ffmpeg`, `ChatBrain`

- OBS WebSocket v5+ installed + configured

- VTube Studio with WebSocket plugin enabled

---

## 🧪 Roadmap / Optional Add-ons

### 🔄 Lore Runtime Engine: Trigger Logic

- Monitors Twitch subs/follows/raids for lore triggers

- Loads `lore_events.json` timeline and flags new `unlocked` states

- Plays mapped narration from `lore_voice.json` using tone/style

- Emits VTS hotkey or OBS scene override (optional)

- Marks progress across sessions with versioning and unlock state persistence

- 🗣️ Lore Voice Line Engine

  - Reads from `lore_voice.json` to play event-specific narration
  - Custom pitch, style, and emotion per milestone
  - Works alongside `lore_events.json` and reacts to Twitch event triggers

- 🔁 Lore Event Visual & Voice Reactions

  - Automatically play voice lines and trigger VTS expressions during lore milestone unlocks
  - Use emotion from `lore_events.json` to choose tone, pitch, and scene animation
  - Optional OBS scene override for special lore events

- 🧬 Lore Event Engine (Milestone Triggers)

  - Script Twitch-based lore events (subs, follows, raids)
  - Stores timeline entries and unlockable lore flags
  - Auto-adjusts character tone and personality per lore milestone
  - Ties into existing `lore_events` memory system

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

