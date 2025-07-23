from pydub import AudioSegment
import re

def align_phonemes_to_lyrics(lyrics):
    words = lyrics.lower().split()
    phoneme_map = {word: re.sub(r'[aeiou]', 'ə', word) for word in words}
    return phoneme_map

def cut_audio_by_phoneme(audio_path, phoneme_map):
    audio = AudioSegment.from_file(audio_path)
    duration = len(audio)
    per_phoneme = duration // len(phoneme_map) if phoneme_map else 1
    segments = {}
    for i, word in enumerate(phoneme_map):
        start = i * per_phoneme
        end = start + per_phoneme
        segments[word] = audio[start:end]
    return segments
