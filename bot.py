import discord
import json

bot = discord.Bot()


with open("config.json") as conf:
    config = json.load(fp=conf)


@bot.event
async def on_ready():
    pass


@bot.event
async def on_message(message):
    pass


cogs_list = [
    "math"
]


for cog in cogs_list:
    bot.load_extension(f"cogs.{cog}")


bot.run(config["token"])
