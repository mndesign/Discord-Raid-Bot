import settings
import discord
import asyncio
import os
from startup import Startup
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix='.', 
    intents=intents, 
    application_id=settings.DISCORD_ID)

os.system('cls' if os.name == 'nt' else 'clear')

@bot.event
async def on_ready():
    Startup()

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message[0] == '.':
        return
    if message.author == bot.user:
        return

async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

async def main():
    await load()
    await bot.start(settings.DISCORD_API)

asyncio.run(main())
