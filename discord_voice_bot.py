# Discord Voice Listener Bot for AI VTuber (Multi-Speaker Enhanced)
import discord
from discord.ext import commands
import asyncio
import os
import threading
import tempfile
import subprocess
from chatbrain_core import ChatBrain

# Voice capture dependencies
import speech_recognition as sr

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)
vc_enabled = {}  # per guild toggle
chatbrain_instances = {}

@bot.event
async def on_ready():
    print(f"[READY] Discord voice bot connected as {bot.user}")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def enablevc(ctx):
    vc_enabled[ctx.guild.id] = True
    await ctx.send("🔊 Voice responses ENABLED.")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def disablevc(ctx):
    vc_enabled[ctx.guild.id] = False
    await ctx.send("🔇 Voice responses DISABLED.")

@bot.command()
async def setmode(ctx, persona: str):
    config_path = "config/settings.json"
    if not os.path.exists(config_path):
        await ctx.send("⚠️ Config file missing.")
        return
    import json
    with open(config_path, "r") as f:
        all_settings = json.load(f)

    # Auto-fill missing switch lines
    defaults = {
        "nova": {
            "switch_expression": "Hotkey_NovaIntro",
            "switch_voice_line": "Now entering Nova protocol."
        },
        "gremlin": {
            "switch_expression": "Hotkey_GremlinIntro",
            "switch_voice_line": "Time to cause some chaos. Gremlin online!"
        },
        "idol": {
            "switch_expression": "Hotkey_IdolIntro",
            "switch_voice_line": "Stage lights on! Idol persona activated."
        },
        "cyber": {
            "switch_expression": "Hotkey_CyberIntro",
            "switch_voice_line": "Cybersync engaged. Tactical mode enabled."
        }
    }
    for k, v in defaults.items():
        if k in all_settings.get("personas", {}):
            all_settings["personas"][k].setdefault("switch_expression", v["switch_expression"])
            all_settings["personas"][k].setdefault("switch_voice_line", v["switch_voice_line"])
    if persona not in all_settings.get("personas", {}):
        await ctx.send(f"❌ Persona '{persona}' not found.")
        return
    memory_mode_path = f"memory/persona_mode_{ctx.guild.id}.json"
    with open(memory_mode_path, "w") as f:
        json.dump({"persona": persona}, f)
    await ctx.send(f"✅ Persona mode switched to '{persona}'.")
    # 🔊 Optional: Visual + voice confirmation
    try:
        import json, asyncio
        with open("config/settings.json", "r") as f:
            all_settings = json.load(f)
        emotion_hotkeys = all_settings.get("vts", {})
        persona_expression = all_settings.get("personas", {}).get(persona, {}).get("switch_expression", "Hotkey_Intro")
        persona_voice = all_settings.get("personas", {}).get(persona, {}).get("switch_voice_line", f"Now assuming {persona} mode.")

        async def vts_trigger_expression(expression):
            import websockets
            await asyncio.sleep(float(emotion_hotkeys.get("blend_delay", 0.1)))
            print(f"[VTS] Persona Mode: Triggering {expression}")
            async with websockets.connect("ws://localhost:8001") as ws:
                await ws.send(json.dumps({
                    "apiName": "VTubeStudioPublicAPI",
                    "requestID": "personaSwitch",
                    "messageType": "HotkeyTriggerRequest",
                    "data": {"hotkeyID": expression}
                }))

        asyncio.create_task(vts_trigger_expression(persona_expression))

        if all_settings.get("vts", {}).get("enable_voice", True):
            guild_id = ctx.guild.id
            if chatbrain_instances.get(guild_id):
                chatbrain_instances[guild_id].speak(
                    persona_voice,
                    voice="nova",
                    pitch=1.0,
                    rate=1.0,
                    style="narration"
                )
    except Exception as switch_feedback_err:
        print(f"[PersonaSwitch] Feedback error: {switch_feedback_err}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        await ctx.send(f"🎙️ Joined {channel.name}.")
        start_listening(vc, ctx.guild.id)
    else:
        await ctx.send("You're not in a voice channel!")

def start_listening(vc, guild_id):
    recognizer = sr.Recognizer()
    source = sr.Microphone()

    def listen_loop():
        with source as mic:
            recognizer.adjust_for_ambient_noise(mic)
            import json
            memory_file = f"memory/voice_speaker_cache_{guild_id}.json"
            if os.path.exists(memory_file):
                with open(memory_file, "r") as f:
                    speaker_cache = json.load(f)
            else:
                speaker_cache = {}
            speaker_counter = len(speaker_cache) + 1

            while True:
                if not vc_enabled.get(guild_id, False):
                    continue
                try:
                    audio = recognizer.listen(mic, timeout=5)
                    text = recognizer.recognize_whisper(audio)
                    speaker_id = hash(audio.frame_data) % 100000

                    # Try to get matching member in voice channel
                    speaker_name = None
                    if vc and vc.channel:
                        for member in vc.channel.members:
                            if not member.bot and member.voice and member.voice.self_mute is False:
                                speaker_name = member.display_name
                                break

                    if speaker_id not in speaker_cache:
                        speaker_cache[speaker_id] = speaker_name or f"user{speaker_counter}"
                        speaker_counter += 1

                    speaker_name = speaker_cache[speaker_id]
                    with open(memory_file, "w") as f:
                        json.dump(speaker_cache, f, indent=2)
                    print(f"[VC] {speaker_name}: {text}")
                    # Decay memory/emotion influence
                    import time
                    memory_decay_path = f"memory/decay_{guild_id}.json"
                    if os.path.exists(memory_decay_path):
                        with open(memory_decay_path, "r") as f:
                            decay_state = json.load(f)
                    else:
                        decay_state = {"last_reset": time.time(), "emotion": "neutral"}

                    now = time.time()
                    if now - decay_state.get("last_reset", 0) > 300:
                        decay_state = {"last_reset": now, "emotion": "neutral"}
                        print("[MEMORY] Emotion decay triggered — resetting to neutral")
                        with open(memory_decay_path, "w") as f:
                            json.dump(decay_state, f, indent=2)

                        # Revert OBS scene
                        try:
                            revert_scene_name = obs_emotion_scenes.get("revert", "Scene_Idle")
                            revert_delay = int(obs_emotion_scenes.get("revert_delay", 10))
                            ws_revert = obsws(host=obs_host, port=obs_port, password=obs_password)
                            ws_revert.connect()
                            ws_revert.call(requests.SetCurrentProgramScene(revert_scene_name))
                            ws_revert.disconnect()
                            print(f"[OBS] [Auto-Revert] to {revert_scene_name}")
                            try:
                                with open("logs/voicebot.log", "a") as log:
                                    log.write(f"[OBS] Reverted to {revert_scene_name} by {speaker_name or 'unknown'} at {time.ctime()} (last emotion: {decay_state.get('emotion', 'unknown')})
")
                            except:
                                pass
                            # Optional: play soft SFX
                            soft_sfx_path = "soundboard/revert_sfx.mp3"
                            if emotion_hotkeys.get("enable_sfx", True) and os.path.exists(soft_sfx_path):
                                os.system(f'start /min wmplayer "{soft_sfx_path}"')
                            # Optional: speak voice line
                            try:
                                if emotion_hotkeys.get("enable_voice", True) and chatbrain_instances.get(guild_id):
                                    memory_mode_path = f"memory/persona_mode_{guild_id}.json"
                                    if os.path.exists(memory_mode_path):
                                        with open(memory_mode_path, "r") as f:
                                            persona = json.load(f).get("persona", "nova")
                                    else:
                                        persona = "nova"
                                    recovery_voice_lines = all_settings.get("personas", {}).get(persona, {}).get("recovery_voice_lines", {
                                        "angry": "Systems calming. Hostility neutralized.",
                                        "shy": "Anxiety decreasing. Regaining confidence.",
                                        "glitch": "Stability restored. Glitch mode disengaged.",
                                        "happy": "Returning to emotional baseline.",
                                        "neutral": "Emotion stabilized. Returning to standby mode."
                                    })
                                    line = recovery_voice_lines.get(decay_state.get("emotion", "neutral"), "Emotion stabilized. Returning to standby mode.")
                                    chatbrain_instances[guild_id].speak(line, voice="nova", pitch=1.0, rate=1.0, style="narration")
                            except Exception as revert_voice_err:
                                print(f"[TTS] Revert voice error: {revert_voice_err}")
                            try:
                                with open("logs/voicebot.log", "a") as log:
                                    log.write(f"[OBS] Voice revert error: {revert_voice_err} from {speaker_name or 'unknown'} at {time.ctime()} (last emotion: {decay_state.get('emotion', 'unknown')})
")
                            except:
                                pass
                        except Exception as revert_err:
                            print(f"[OBS] Auto-Revert failed: {revert_err}")

                        # Revert VTS expression
                        try:
                            asyncio.create_task(vts_trigger_expression(emotion_hotkeys.get("fallback", "Hotkey_Neutral")))
                        except Exception as vts_fallback_err:
                            print(f"[VTS] Auto-Revert failed: {vts_fallback_err}")
                        else:
                            print("[VTS] Auto-Revert: Expression fallback triggered")
                            try:
                                with open("logs/voicebot.log", "a") as log:
                                    log.write(f"[VTS] Reverted to fallback expression by {speaker_name or 'unknown'} at {time.ctime()} (last emotion: {decay_state.get('emotion', 'unknown')})
")
                            except:
                                pass
                            soft_sfx_path = "soundboard/revert_sfx.mp3"
                            if os.path.exists(soft_sfx_path):
                                os.system(f'start /min wmplayer "{soft_sfx_path}"')
                            try:
                                if emotion_hotkeys.get("enable_voice", True) and chatbrain_instances.get(guild_id):
                                    persona = "nova"
                                visual_recovery_lines = all_settings.get("personas", {}).get(persona, {}).get("visual_recovery_lines", {
                                    "glitch": "Restoring stable frame output.",
                                    "angry": "Retuning visuals to calm.",
                                    "shy": "Expressions settling. Visuals normalized.",
                                    "happy": "Ending expressive feedback.",
                                    "neutral": "Visual systems returning to baseline."
                                })
                                vts_line = visual_recovery_lines.get(decay_state.get("emotion", "neutral"), "Visual systems returning to baseline.")
                                chatbrain_instances[guild_id].speak(vts_line, voice="nova", pitch=1.0, rate=1.0, style="narration")
                            except Exception as vts_revert_voice_err:
                                print(f"[TTS] VTS revert voice error: {vts_revert_voice_err}")
                            try:
                                with open("logs/voicebot.log", "a") as log:
                                    log.write(f"[VTS] Voice revert error: {vts_revert_voice_err} from {speaker_name or 'unknown'} at {time.ctime()} (last emotion: {decay_state.get('emotion', 'unknown')})
")
                            except:
                                pass
                    if now - decay_state.get("last_reset", 0) > 300:  # every 5 mins
                        decay_state = {"last_reset": now, "emotion": "neutral"}
                        print("[MEMORY] Emotion decay triggered — resetting to neutral")
                        with open(memory_decay_path, "w") as f:
                            json.dump(decay_state, f, indent=2)

                    # Estimate loudness (volume intensity)
                    volume_level = max(audio.frame_data) if hasattr(audio, 'frame_data') else 128
                    intensity = "calm"
                    if volume_level > 192:
                        intensity = "excited"
                    elif volume_level < 96:
                        intensity = "whispery"

                    # Ensure tone is mapped consistently across get_response and speak
                    tone_style_map = {
                        "excited": "excited",
                        "whispery": "whisper",
                        "calm": "narration"
                    }

                    reply, emotion, voice, lore_events = chatbrain_instances[guild_id].get_response(
                        text,
                        username=speaker_name,
                        tone_override=intensity
                    )

                    # 🔌 VTS WebSocket: Trigger expression by emotion
                    # 🎛️ OBS WebSocket: Trigger scene by emotion
                    try:
                        import obswebsocket
                        from obswebsocket import obsws, requests

                        import json
                        config_path = "config/settings.json"
                        default_config = {
                            "obs": {
                                "happy": "Scene_Happy",
                                "angry": "Scene_Angry",
                                "shy": "Scene_Shy",
                                "glitch": "Scene_GlitchMode",
                                "revert": "Scene_Idle",
                                "revert_delay": 10
                            }
                        }
                        if os.path.exists(config_path):
                            with open(config_path, "r") as f:
                                settings = json.load(f)
                        else:
                            settings = default_config
                            os.makedirs(os.path.dirname(config_path), exist_ok=True)
                            with open(config_path, "w") as f:
                                json.dump(default_config, f, indent=2)

                        obs_emotion_scenes = settings.get("obs", {})
                        else:
                            obs_emotion_scenes = default_scene_map
                            os.makedirs(os.path.dirname(config_path), exist_ok=True)
                            with open(config_path, "w") as f:
                                json.dump(default_scene_map, f, indent=2)

                        obs_host = "localhost"
                        obs_port = 4455  # default OBS WebSocket v5 port
                        obs_password = os.getenv("OBS_PASSWORD", "")

                        scene_keys = [e.strip() for e in emotion.split("+")]
                        triggered_obs = False

                        for key in scene_keys:
                            if key in obs_emotion_scenes:
                                scene_name = obs_emotion_scenes[key]
                                try:
                                    ws = obsws(host=obs_host, port=obs_port, password=obs_password)
                                    ws.connect()
                                    ws.call(requests.SetCurrentProgramScene(scene_name))
                                    # Load revert scene name and delay from config
                                    revert_scene_name = obs_emotion_scenes.get("revert", "Scene_Idle")
                                    revert_delay = int(obs_emotion_scenes.get("revert_delay", 10))
                                    async def revert_scene():
                                        await asyncio.sleep(revert_delay)
                                        try:
                                            ws_revert = obsws(host=obs_host, port=obs_port, password=obs_password)
                                            ws_revert.connect()
                                            ws_revert.call(requests.SetCurrentProgramScene(revert_scene_name))
                                            ws_revert.disconnect()
                                            print(f"[OBS] Reverted to {revert_scene_name}")
                                        except Exception as revert_err:
                                            print(f"[OBS] Revert failed: {revert_err}")
                                    asyncio.create_task(revert_scene())
                                    ws.disconnect()
                                    print(f"[OBS] Switched to scene: {scene_name}")
                                    triggered_obs = True
                                except Exception as obs_err:
                                    print(f"[OBS] Scene switch failed: {obs_err}")

                        if not triggered_obs:
                            print("[OBS] No matching scene, fallback ignored.")

                    except Exception as obs_global_error:
                        print(f"[OBS] General OBS WebSocket error: {obs_global_error}")
                    try:
                        import asyncio
                        import websockets
                        async def vts_trigger_expression(expression):
                            await asyncio.sleep(float(emotion_hotkeys.get("blend_delay", 0.1)))  # slight delay to ensure blend
                            print(f"[VTS] Triggering: {expression}")
                            async with websockets.connect("ws://localhost:8001") as ws:
                                await ws.send(json.dumps({
                                    "apiName": "VTubeStudioPublicAPI",
                                    "requestID": "triggerExpression",
                                    "messageType": "HotkeyTriggerRequest",
                                    "data": {"hotkeyID": expression}
                                }))
                        import json
                        hotkey_path = "config/settings.json"
                        default_hotkeys = {
                            "vts": {
                                "happy": "Hotkey_HappyFace",
                                "angry": "Hotkey_Angry",
                                "shy": "Hotkey_Blush",
                                "glitch": "Hotkey_GlitchMode",
                                "fallback": "Hotkey_Neutral",
                                "blend_delay": 0.1
                            }
                        }
                        if os.path.exists(hotkey_path):
                            with open(hotkey_path, "r") as f:
                                all_settings = json.load(f)
                        else:
                            all_settings = default_hotkeys
                            os.makedirs(os.path.dirname(hotkey_path), exist_ok=True)
                            with open(hotkey_path, "w") as f:
                                json.dump(default_hotkeys, f, indent=2)

                        emotion_hotkeys = all_settings.get("vts", {})
                        else:
                            emotion_hotkeys = default_hotkeys
                            os.makedirs(os.path.dirname(hotkey_path), exist_ok=True)
                            with open(hotkey_path, "w") as f:
                                json.dump(default_hotkeys, f, indent=2)
                        emotion_keys = [e.strip() for e in emotion.split("+")]
                        matched = False
                        for i, key in enumerate(emotion_keys):
                            if key in emotion_hotkeys:
                                asyncio.create_task(vts_trigger_expression(emotion_hotkeys[key]))
                                matched = True
                        if not matched:
                            asyncio.create_task(vts_trigger_expression(emotion_hotkeys.get("fallback", "Hotkey_Neutral")))  # Fallback to neutral face
                    except Exception as vts_err:
                        print(f"[VTS] WebSocket error: {vts_err}")

                    # React to lore events using tone
                    if lore_events:
                        for event in lore_events:
                            print(f"[LORE] Reacting to: {event} (tone: {intensity})")
                            # You can add lore overlay, animation or log logic here
                    if speaker_name:
                        reply = f"{speaker_name}, {reply}"
                    import json
                    style_path = "config/voice_styles.json"
                    style_settings = {
                        "pitch": 1.0,
                        "rate": 1.0,
                        "style": tone_style_map.get(intensity, "narration")
                    }
                    if os.path.exists(style_path):
                        with open(style_path, "r") as f:
                            styles = json.load(f)
                            style_settings.update(styles.get(intensity, {}))

                    try:
                        chatbrain_instances[guild_id].speak(
                            reply,
                            voice,
                            pitch=style_settings["pitch"],
                            rate=style_settings["rate"],
                            style=style_settings["style"]
                        )
                    except Exception as speak_err:
                        print(f"[FALLBACK] TTS failed: {speak_err}")
                        fallback_reply = f"[{voice.upper()}] {reply}"
                        print(fallback_reply)
                        # Optional: play fallback sound effect
                        fallback_sound = "soundboard/tts_fallback.mp3"
                        if emotion_hotkeys.get("enable_sfx", True) and os.path.exists(fallback_sound):
                            os.system(f'start /min wmplayer "{fallback_sound}"')
                except Exception as e:
                    print(f"[ERROR] VC listen: {e}")

    threading.Thread(target=listen_loop, daemon=True).start()

@bot.event
async def on_guild_join(guild):
    chatbrain_instances[guild.id] = ChatBrain(channel_id=f"discord_{guild.id}")

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)
