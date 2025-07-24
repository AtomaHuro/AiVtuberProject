<img width="1536" height="1024" alt="ChatGPT Image Jul 14, 2025, 08_35_01 PM" src="https://github.com/user-attachments/assets/eff918d6-4d19-433c-b0f6-d2f720c74bcc" />

## ✅ Core Feature Overview

### 🎙️ Voice & Emotion Recognition

**Path:** `modules/voice/`

- Uses Whisper to detect tone, speaker identity
- Emotion classification feeds into memory, voice modulation
- Discord listener supports multi-speaker memory tagging
- Emotion-to-TTS mapping for expressive speech
- Voice activity linked to viewer emotion reactions
- Night mode auto-switch based on time or ambient emotion

### 🎭 Personality & Mode Switching

**Path:** `modules/persona/`

- Supports `/setmode`, raid/sub/milestone triggers
- AI auto-adjusts personality per chat sentiment or voice tone
- Viewers influence persona shifts (cute, gremlin, emotion-bound)
- Viewer influence decays over time; modifiers stored across sessions
- Discord speaker influence support

### 🧠 Memory Engine (Persistent)

**Path:** `memory/`, `modules/memory/`

- JSON per channel/server, encrypted & autosaved periodically
- Tracks viewers by tone, frequency, tags (toxic, flirty, loyal)
- Decay-based priority aging with resurfacing boost
- Relationship memory building (fan, rival, friend)
- Lore-unlock progression and memory corruption fallback support

### 💬 ChatBrain + LLM Integration

**Path:** `core/chatbrain.py`

- Injects emotion, memory, persona, lore tags into GPT/local LLM
- Supports tone-bound phrasing: sarcasm, flirty, hype, etc.
- Memory corruption injection logic and alternate persona hooks
- Trigger keywords (e.g., “glitch”, “why were you made”) redirect behavior
- GPT + local fallback integration with token usage tracking

### 📺 OBS / VTube Studio Integration

**Path:** `modules/obs/`, `modules/vts/`

- Scene overlays for emotion (blush, glitch, angry face, tears)
- VTS WebSocket plugin to trigger expressions and animations
- Mode shifts sync with stream scenes (night mode, emotion matches)
- Audio-visual glitch events driven by corruption level

### 🎶 AI Singing System

**Path:** `modules/singing/`

- Extracts phonemes, pitch from YouTube music videos
- Builds adaptive melody memory by emotion and mode
- Supports corruption glitch stutter, pitch shift, phrasing errors
- Persona-voice-shifted lyric performance via ElevenLabs or local

### 🔊 TTS + Audio Engine

**Path:** `modules/tts/`

- ElevenLabs main, Edge-TTS + gTTS as fallback, routed via VB-Audio
- Emotion-aligned pitch, speed, tone variation
- Saves `.wav` or `.mp3` for OBS overlays or triggers
- Queue system & async audio for Discord, Twitch playback
- Realtime auto-swap TTS voice by mode/persona

### 📋 GUI Control Dashboard (React)

**Path:** `gui/`

- `CorruptionControlPanel.jsx` — glitch injection, recovery, decay meter
- `GlitchLogControlPanel.jsx` — glitch events viewer and logger
- Sidebar + route-linked modular React UI
- Dark terminal-styled design, toggleable refresh + clear buttons
- Optional remote control via auth-verified moderator login

---

## 🧬 Memory Corruption Engine

**Path:** `modules/corruption/`

- Emotion overload triggers glitch tone and alt persona
- Decay logic auto-reduces corruption on calm interactions
- Voice distortion system (glitch speech, phoneme damage)
- Lore-injection: hallucinations, timelines, denial reactions
- UI-triggerable + Twitch/Discord-reactive triggers

---

## 🧪 Optional & Experimental Modules

| Module                       | Description                                                   |
| ---------------------------- | ------------------------------------------------------------- |
| Lore Timeline GUI            | View unlock history, triggered arcs, persona phases           |
| Remote Auth                  | OAuth Twitch/YouTube moderator login for control panel access |
| Prompt Analytics             | Token tracking, chat interaction heatmap                      |
| Stream Cluster Sync          | Multi-AI character sync over networked Twitch events          |
| Singing Overlay              | Real-time lyric bouncing UI with expression detection         |
| Persona Matching             | AI mimics viewer tone or sarcasm (training via chat)          |
| Alternate Memory Threads     | Remembers conflicting beliefs under personas or corruption    |
| Discord Speaker Tone Shifter | Adapts voice style by who's speaking in VC                    |
| Soundboard Emotional Hooks   | Emotional SFX hotkeys per mode                                |

---

## 🚀 Future Ideas

| Feature                            | Description                                                 |
| ---------------------------------- | ----------------------------------------------------------- |
| **Adaptive Memory Prioritization** | Older, irrelevant memories decay unless resurfaced          |
| **Conversational Thread Recall**   | Maintains multi-turn memory across user chats               |
| **Viewer Relationship Memory**     | AI builds rival/friend/fan bonds with viewers               |
| **Sarcasm/Irony Detection**        | Learns to react to memes, sarcasm, in-jokes                 |
| **Dream Mode**                     | AI generates surreal "dream logs" at night from lore/memory |
| **Phantom AI Doppelgänger**        | Rare glitches that contradict main lore/personality         |
| **Live Poll Personality Events**   | Twitch polls trigger story path/persona choices             |
| **Emotion Feedback Voting**        | Viewers rate if response matched emotional context          |
| **AI Memory Regeneration**         | Memory files partially self-heal over time                  |
| **Adaptive Singing Persona**       | Singing changes per viewer or stream style                  |
| **Remote Viewer Role Assignment**  | AI gives nicknames/roles to frequent viewers                |

---

## 📁 Full Project Structure

```bash
├── core/
│   └── chatbrain.py                          # Central AI logic (memory, persona, speaking)
│
├── twitch/
│   └── twitch_listener_bot.py                # Twitch EventSub + emotion hooks
│
├── youtube/
│   └── youtube_listener_bot.py               # (Optional) YouTube Live Chat relay integration
│
├── discord/
│   └── discord_listener.py                   # Discord voice & emotion listener
│
├── modules/
│   ├── voice/
│   │   ├── emotion_detector.py
│   │   └── discord_listener.py
│   ├── memory/
│   │   ├── memory_manager.py                     # Memory system & viewer relationship storage
│   │   ├── memory_integrity.json                 # Persistence & corruption awareness
│   │   └── corruption_persona.json               # Alternate persona memory patterns
│   ├── persona/
│   │   ├── mode_switcher.py                      # Personality mode triggers & logic
│   │   └── persona_profiles.json                 # Profiles and emotional behaviors
│   ├── tts/
│   │   ├── eleven_wrapper.py                     # Primary TTS engine (ElevenLabs)
│   │   ├── edge_fallback.py                      # Fallback TTS engine (Edge-TTS)
│   │   └── audio_router.py                       # Handles playback routing (Voicemeeter/WMP/etc)
│   ├── singing/
│   │   ├── melody_learner.py                     # Adaptive AI singing from video/audio
│   │   └── phoneme_aligner.py                    # Sync lyrics + pitch to voice
│   ├── obs/
│   │   └──obs_websocket_service.py              # OBS integration for emotional visuals
│   ├── vts/
│   │   └── vts_websocket_bridge.py               # VTube Studio WebSocket emotion triggers
│   └── corruption/
│       ├── glitch_injector.py
│       ├── corruption_decay.py
│       └── glitch_log.json
│
├── gui/
│   ├── App.jsx                               # React GUI entry
│   ├── Sidebar.jsx                           # Sidebar nav
│   ├── CorruptionControlPanel.jsx            # Controls glitch mode + persona corruption
│   ├── GlitchLogControlPanel.jsx             # Displays glitched memories
│   ├── style.css
│   └── dark_theme.css
│
├── remote_control/
│   ├── RemoteControlTerminalUI.py            # Remote mod/admin terminal
│   ├── launch_auth_server.bat
│   ├── launch_remote_control.bat
│   └── system_monitor.bat
|
├── configs/
│   ├── decay_config.json                     # Settings for corruption decay over time
│   └── persona_modes.json                    # All available preset modes and mappings
│
├── assets/
│   └── audio_clips/                          # Saved generated voice clips (.wav/.mp3)
│
├── logs/
│   └── glitch_log.json                       # Tracks glitch corruption events
├── auth/
│   └── remote_auth_server.py
|
├── tools/
│   ├── ngrok_setup.bat                       # Launch tunnel for Twitch EventSub
│   └── ffmpeg_router.bat                     # Audio streaming support
```

<img width="1024" height="1536" alt="ChatGPT Image Jul 14, 2025, 08_08_59 PM" src="https://github.com/user-attachments/assets/801d9403-ca91-4d7c-8c8d-f7f1a79a190a" />

---

## 📦 Remote Tools

- `launch_auth_server.bat` → Twitch/YouTube OAuth moderator check
- `launch_remote_control.bat` → Minimal UI control from other IP
- `RemoteControlTerminalUI.py` → Command-line interface from outside machine

---

## 💻 Requirements

- Python 3.9+
- Node.js + React
- `discord.py`, `flask`, `whisper`, `obs-websocket-py`
- `elevenlabs`, `edge-tts`, `yt-dlp`, `librosa`
- VB-Audio Cable / Voicemeeter (for audio routing)

---

## 🧠 Dev Snippet

```py
chatbrain_instances[guild_id] = ChatBrain(channel_id=f"discord_{guild_id}")
```

---


> ✅ This README is auto-updated as new modules and features are implemented. You may script auto-updates from the module generator pipeline.

