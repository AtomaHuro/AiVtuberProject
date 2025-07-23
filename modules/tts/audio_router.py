import os
import platform

def play_audio(path):
    system = platform.system()
    if system == "Windows":
        os.system(f'start /min wmplayer "{path}"')
    elif system == "Darwin":
        os.system(f"afplay '{path}'")
    else:
        os.system(f"ffplay -nodisp -autoexit '{path}'")
