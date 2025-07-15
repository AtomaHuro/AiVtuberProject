# 🧠 AI VTuber Discord Voice Listener

A multi-personality, multi-speaker-enabled AI VTuber system designed for full emotion-aware interaction — blending Discord voice input, Twitch triggers, OBS/VTube Studio visuals, ChatBrain AI memory, singing synthesis, and real-time emotional states.

---

## ✅ Core Features

### 🔊 Voice Capture & Emotion Detection

- 🎙️ Listens in real-time to Discord calls via Whisper
- 🧠 Identifies speaker and saves per-user emotion memory
- 💬 Adjusts tone and reaction based on detected vocal intensity or emotion
- 👥 Supports multi-speaker interactions with unique per-user response shifts

### 🎭 Personality Modes & Expression Mapping

- 🔁 `/setmode <persona>` live personality switching
- 🧬 Persona-based tone, overlay, and voice line bundles
- 🎨 Visual + voice confirmation via OBS/VTube Studio integration

### 📺 OBS & VTube Studio Integration

- 🎥 Emotion-mapped scene switching (e.g. glitch, happy, sleepy)
- 🎭 WebSocket-linked VTS expression overlays
- 🕓 Auto-reset to neutral after decay timers
- 🧠 Persistent expression memory & GUI controls

### 🧠 ChatBrain + LLM Interaction

- 💬 Twitch + Discord chat interpreted through GPT/local LLM
- 🧬 Context-aware lore injection and memory tags
- 🔑 Trigger-word → tone/emotion/persona reaction
- 🗃️ Fallback system for memory corruption, recovery, or persona shift

### 🎶 AI Singing Engine

- 🎵 Learns melodies from YouTube links
- 🔊 Auto-generates voice previews using emotion-matched TTS
- 🧑‍🎤 Sing mode includes `/previewmelody` + GUI dropdown

### 🎙️ TTS Integration (VoiceAI / ElevenLabs / Edge)

- 🗣️ Emotion-mapped pitch + speaking rate
- 📁 Voice responses saved to `.mp3` or `.wav` for OBS
- 🔁 Fallback/recovery speech triggered on failure

### 💻 GUI Dashboard

- 🎛️ Dropdowns for mood/persona/expression
- 🔁 Live expression state polling (every 5s)
- ✅ Trigger feedback preview

### 🔒 Memory & Lore

- 💾 Corruption-aware memory system (`memory_integrity.json`)
- 🧬 Mood-driven lore progression
- 📖 `lore_events.json` and `lore_voice.json` tied to Twitch milestones
- 🔐 Encrypted/autosaved JSON files per session/channel

---

## 📁 Folder Structure

```txt
├── memory/
│   ├── corruption_persona.json   # Alternate personalities
│   ├── corrupted_voice.json      # Glitched tone speech
│   ├── memory_integrity.json     # Corruption % and logs
│   ├── lore_events.json          # Lore triggers
│   ├── lore_voice.json           # Emotion-linked voice packs
│   ├── sing_profile.json         # Learned melodies
│   ├── sing_menu.json            # GUI menu
│   ├── last_expression.json      # Last emotion/face used
│   └── decay_*.json              # Emotion decay
├── config/
│   ├── settings.json             # Persona maps
│   ├── vts_expressions.json      # Face triggers
│   └── voice_styles.json         # Emotion → pitch/style
├── logs/
│   └── voicebot.log              # Events + errors
├── soundboard/
│   ├── revert_sfx.mp3
│   └── tts_fallback.mp3
```

---

## 🧬 Memory Corruption Engine (Active)

- ⚠️ Triggers alternate persona + glitch tones when emotional overload occurs
- 🎭 Injects corrupted dialogue into ChatBrain
- ⏱️ Timed recovery, or mod-triggered restore
- 📉 Decay logic auto-reduces corruption during calm
- 🎙️ Glitched voices + visual glitch effects via OBS/VTS

---

## 🧪 Optional & Advanced Modules

- 📖 Lore Timeline Viewer GUI
- 🎵 Singing Overlay Sync w/ Bouncing Lyrics
- 📊 Stream Analytics (viewer mood tracking)
- 🔄 Emotion Decay Speed Editor
- 🔁 Randomized Auto-Moods
- 🧩 Trigger Word to Emotion Mapping
- 🌐 Stream Audience Voting (public mood system)
- 🧠 Prompt History Viewer
- 🗣️ Multi-language Voice Switch

---

## 🧵 Dev Notes

> Part of the **Ai VTuber Core Stack**. Built for immersive streaming and emotionally reactive AI.

### 🧠 LLM Example Init

```py
chatbrain_instances[guild_id] = ChatBrain(channel_id=f"discord_{guild_id}")
```

---

## 🛠️ Requirements

- Python 3.9+
- Discord.py, Whisper, ffmpeg
- OBS WebSocket v5+, VTube Studio + plugin
- Node.js (GUI)
- ChatBrain (OpenAI or local LLM)

---

## 🖼 GitHub Enhancements

&#x20;&#x20;

> ✨ You can also use [GitHub Pages](https://pages.github.com/) to present this README beautifully with themes.

---

## 📞 Support

Need help? Ping for OBS/VTS wiring, GUI linking, or Discord voice configs.

