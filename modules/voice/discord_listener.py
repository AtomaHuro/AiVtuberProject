import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"[Discord] Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    print(f"[Discord] {message.author.name}: {message.content}")
    await bot.process_commands(message)

def start_discord_bot(token):
    bot.run(token)
