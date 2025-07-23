# memory_manager.py
import json
from pathlib import Path
import os

class MemoryManager:
    def __init__(self, path="memory/memory_integrity.json"):
        self.path = path
        self.data = {}
        self.load()

    def load(self):
        if Path(self.path).exists():
            with open(self.path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def update_viewer_tag(self, viewer, tag, value=1, reason=None):
        if viewer not in self.data:
            self.data[viewer] = {}
        if "tags" not in self.data[viewer]:
            self.data[viewer]["tags"] = {}
        self.data[viewer]["tags"][tag] = {
            "value": value,
            "reason": reason
        }
        self.save()
