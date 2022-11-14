import discord
import json


bot = discord.Bot()


with open("config.json") as conf:
    config = json.load(fp=conf)


class PollMenu(discord.ui.View):
    def __init__():
        super().__init__()
    
    


@bot.event
async def on_ready():
    pass


@bot.event
async def on_message(message):
    pass


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


cogs_list = [
    "math",
    "bomb_tag",
    "poll"
]


for cog in cogs_list:
    bot.load_extension(f"cogs.{cog}")


bot.run(config["token"])
