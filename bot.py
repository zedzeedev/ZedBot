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


@bot.command(description="Forces the bot to send the given message.")
async def talk(ctx, msg: str):
    await ctx.respond("Message sending...", ephemeral=True)
    await ctx.send(msg)


cogs_list = [
    "math",
    "games.connect_four",
    "poll"
]


for cog in cogs_list:
    bot.load_extension(f"cogs.{cog}")

bot.run(config["token"])
