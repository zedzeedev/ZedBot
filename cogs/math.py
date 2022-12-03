import discord
from discord.ext import commands
from math import sqrt


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(name="sum", description="Adds two numbers together")
    async def sum(self, ctx, num1: float, num2: float):
        await ctx.respond(num1 + num2)

    @discord.slash_command(name="sqrt", description="Square root of a number")
    async def sqrt(self, ctx, num: float):
        await ctx.respond(sqrt(num))

    @discord.slash_command(name="pow", description="Raises a number to a given power")
    async def pow(self, ctx, num: float, power: float):
        await ctx.respond(num**power)


def setup(bot):
    bot.add_cog(Math(bot=bot))
