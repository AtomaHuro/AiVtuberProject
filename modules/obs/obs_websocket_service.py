# obs_websocket_service.py
# Sends expression changes to OBS/VTube Studio via WebSocket

import asyncio
import websockets
import json

async def send_obs_command(command: dict):
    uri = "ws://localhost:4455"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(command))
            print(f"[OBS] Sent: {command}")
            response = await websocket.recv()
            print(f"[OBS] Response: {response}")
    except Exception as e:
        print(f"[OBS ERROR] {e}")

# Sample emotion trigger handler
def trigger_emotion_visual(emotion):
    obs_commands = {
        "happy": {"request-type": "TriggerHotkeyByName", "hotkeyName": "OBS_Happy"},
        "angry": {"request-type": "TriggerHotkeyByName", "hotkeyName": "OBS_Angry"},
        "glitched": {"request-type": "TriggerHotkeyByName", "hotkeyName": "OBS_Glitch"},
    }
    if emotion in obs_commands:
        asyncio.run(send_obs_command(obs_commands[emotion]))
