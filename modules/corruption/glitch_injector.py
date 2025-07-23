def inject_glitch(memory, severity=1):
    glitch_text = "[glitched output corrupted by internal loop]"
    memory["glitches"].append({"text": glitch_text, "severity": severity})
    return glitch_text
