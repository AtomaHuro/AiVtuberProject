# 🎭 AI VTuber System — Feature Overview

A fully modular, emotionally responsive, lore-driven AI VTuber inspired by Neuro-sama — with real-time voice, Discord, Twitch/YouTube chat integration, memory, and emotional intelligence.

---

## ✅ Core Features

### 🧠 ChatBrain AI Engine
- GPT + local LLM integration
- Emotion tagging & contextual memory
- Viewer-triggered personalities (/setmode cute, gremlin, etc.)
- Keyword-based reaction triggers
- Auto-generated evolving backstory
- Alternate personality modes + memory corruption arcs
- Lore-aware response engine
- Lore evolves with time and Twitch events

---

## 🎤 Voice & TTS System
- ElevenLabs + Edge-TTS fallback
- Pitch/rate/style mapped from emotional tone
- Supports tone mapping (excited, whispery, calm, etc.)
- Async voice playback + export to `.wav/.mp3`
- Voicemeeter/VB-Audio compatible
- Fallback system + soundboard SFX if TTS fails

---

## 📡 Discord Voice Listener
- Persistent voice listener with `/join`
- Multi-speaker recognition and tracking
- Discord username memory + emotion tracking
- Personality adapts to speaking tone
- Custom TTS tone/style per speaker tone
- `/enablevc` and `/disablevc` for mod control

---

## 📺 Streaming + Chat Integration
- TwitchIO listener + chat interaction
- YouTube Live chat relay
- Viewer-triggered moods and personalities
- Lore tied to Twitch subs, follows, raids
- Personality/mood decay system
- Emotion overlays & stream triggers (in progress)

---

## 📁 Memory System
- Per-user & per-channel long-term memory
- Speaker mapping (voice fingerprint to username)
- Autosave + disk caching of memory & configs
- Emotion-lore consistency over time
- Config auto-generator + fallback support

---

## 📊 Lore System
- Timeline tracking + unlockable lore
- Viewer-triggered events remembered over time
- Lore voice reactions vary by tone
- Alternate personalities can emerge on stream
- Recovery arcs + immersion-boosted responses

---

## 🔧 Config & Tools
- `voice_styles.json` for pitch/rate/style per emotion
- Soundboard generator (`generate_soundboard.py`)
- Voice preview tool (`test_voice_styles.py`)
- Bat launcher with voice synthesis + Discord listener

---

Built for OBS/VTube Studio compatibility. Supports direct audio injection + Twitch reactive events.