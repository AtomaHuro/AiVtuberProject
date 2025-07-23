import re

def detect_emotion(text):
    emotion_keywords = {
        "happy": ["yay", "awesome", "great", "nice", "love"],
        "sad": ["sad", "depressed", "unhappy", "cry", "sorrow"],
        "angry": ["angry", "mad", "furious", "rage"],
        "scared": ["scared", "afraid", "fear", "terrified"],
        "surprised": ["wow", "what", "really", "no way", "surprised"]
    }

    text = text.lower()
    for emotion, keywords in emotion_keywords.items():
        for keyword in keywords:
            if re.search(rf"\b{keyword}\b", text):
                return emotion
    return "neutral"
