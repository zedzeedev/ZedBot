import discord
import json
from time import sleep

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


@bot.command()
async def lesbian(ctx):
    await ctx.respond("yeah, thats me")


@bot.command(description="Forces the bot to send the given message.")
async def talk(ctx, msg: str):
    await ctx.respond("Message sending...", ephemeral=True)
    await ctx.send(msg)


@bot.command(description="WARNING: DO NOT USE")
async def avery(ctx):
    for i in range(0, 100):
        await ctx.respond("omg thats so fucking hot")


bot.run(config["token"])
