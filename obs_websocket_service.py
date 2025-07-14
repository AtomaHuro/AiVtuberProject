# obs_websocket_service.py
# Simple OBS WebSocket interface for AI VTuber reactions

import asyncio
import os
from obswebsocket import obsws, requests
from dotenv import load_dotenv

load_dotenv()

OBS_HOST = os.getenv("OBS_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", 4455))
OBS_PASSWORD = os.getenv("OBS_PASSWORD", "")

class OBSController:
    def __init__(self):
        self.ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)

    def connect(self):
        try:
            self.ws.connect()
            print(f"[OBS] Connected to {OBS_HOST}:{OBS_PORT}")
        except Exception as e:
            print(f"[OBS ERROR] {e}")

    def show_overlay(self, source_name: str, duration: float = 5.0):
        try:
            self.ws.call(requests.SetSceneItemEnabled(source=source_name, scene_name="Main", enabled=True))
            print(f"[OBS] Showing overlay: {source_name}")
            asyncio.create_task(self.hide_overlay_later(source_name, duration))
        except Exception as e:
            print(f"[OBS ERROR] Show overlay: {e}")

    async def hide_overlay_later(self, source_name: str, delay: float):
        await asyncio.sleep(delay)
        try:
            self.ws.call(requests.SetSceneItemEnabled(source=source_name, scene_name="Main", enabled=False))
            print(f"[OBS] Hiding overlay: {source_name}")
        except Exception as e:
            print(f"[OBS ERROR] Hide overlay: {e}")

    def disconnect(self):
        self.ws.disconnect()
        print("[OBS] Disconnected")

if __name__ == "__main__":
    controller = OBSController()
    controller.connect()

    # Example usage
    controller.show_overlay("LoreUnlockOverlay", duration=6.0)

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        controller.disconnect()
