from setuptools import setup, find_packages

setup(
    name="chatbrain-vtuber",
    version="0.1.0",
    description="AI VTuber brain with emotion, lore, glitch mechanics, and TTS integration",
    author="YourName",
    packages=find_packages(),
    install_requires=[
        "openai",
        "elevenlabs",
        "edge-tts",
        "gtts",
        "obs-websocket-py"
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "chatbrain-run = chatbrain.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8'
)
