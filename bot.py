import discord
from discord.ext import commands
import json


with open("testing_config.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.default())

cogs = [
    "math",
    "poll",
    "dplace",
    "games.connect_four",
    "games.tic_tac_toe",
    "games.blackjack"
]

@bot.event
async def setup_hook():
    # Load cogs
    
    for cog in cogs:
        await bot.load_extension("cogs." + cog)
    await bot.tree.sync()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


bot.run(token=token)
