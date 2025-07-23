import time

def decay_corruption(memory, rate=0.01):
    memory["corruption_level"] = max(0, memory.get("corruption_level", 0) - rate)
    memory["last_decay"] = time.time()
    return memory["corruption_level"]
