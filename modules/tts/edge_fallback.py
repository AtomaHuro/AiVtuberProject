import asyncio
import edge_tts

async def generate_edge_tts(text, voice="en-US-AriaNeural", rate="+0%"):
    output = "edge_output.mp3"
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(output)
    return output
