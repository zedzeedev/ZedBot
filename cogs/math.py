import discord
from discord.ext import commands
from math import sqrt

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(description="Adds two numbers together")
    async def sum(self, ctx, num1: float, num2: float):
        await ctx.respond(num1 + num2)

    @discord.slash_command(description="Square root of a number")
    async def sqarert(self, ctx, num: float):
        await ctx.respond(sqrt(num))


def setup(bot):
    bot.add_cog(Math(bot=bot))
