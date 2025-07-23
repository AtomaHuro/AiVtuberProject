# mode_switcher.py
class PersonaEngine:
    def __init__(self):
        self.mode = "default"

    def adjust_from_event(self, event_type, viewer, weight=0.1):
        print(f"[PERSONA] Adjusting persona from {event_type} by {viewer} (weight={weight})")
