import requests
import os

def generate_eleven_audio(text, voice_id="Rachel", emotion="neutral"):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": emotion
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        with open("tts_output.wav", "wb") as f:
            f.write(response.content)
        return "tts_output.wav"
    return None
