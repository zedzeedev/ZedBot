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


stop_cmd = False
@bot.command(description="WARNING: DO NOT USE")
async def avery(ctx):
    stop_cmd = False
    if stop_cmd == False:
        for i in range(0, 100):
            if stop_cmd == True:
                break
            else:
                await ctx.respond("omg thats so fucking hot")
        stop_cmd = True
    else:
        await ctx.respond("stopped")


@bot.command(description="stops the madness")
async def stop(ctx):
    stop_cmd = True
    await ctx.respond("stopped the madness")


bot.run(config["token"])
