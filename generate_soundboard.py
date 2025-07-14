import asyncio
import edge_tts
import os

# Phrases and filenames
clips = {
    "cheer": "Let's gooo! Woo!",
    "boo": "Boooooo!",
    "laugh": "Haha! That was hilarious!",
    "lore_unlock": "A new piece of my lore has been revealed.",
    "raid_alert": "Raid incoming! Brace yourself!",
    "mode_shift": "Shifting into a new personality mode."
}

os.makedirs("soundboard", exist_ok=True)

async def generate_clip(name, text):
    filepath = f"soundboard/{name}.mp3"
    communicate = edge_tts.Communicate(text=text, voice="en-US-AriaNeural")
    await communicate.save(filepath)
    print(f"[✓] Saved: {filepath}")

async def main():
    tasks = [generate_clip(name, text) for name, text in clips.items()]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())