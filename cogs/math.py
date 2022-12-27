import discord
from discord.ext import commands
from discord import app_commands
from math import sqrt


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="sum", description="Adds two numbers together")
    async def sum(self, interaction: discord.Interaction, num1: float, num2: float):
        await interaction.response.send_message(num1 + num2)

    @app_commands.command(name="sqrt", description="Square root of a number")
    async def sqrt(self, interation: discord.Interaction, num: float):
        await interation.response.send_message(sqrt(num))

    @app_commands.command(name="pow", description="Raises a number to a given power")
    async def pow(self, interaction: discord.Interaction, num: float, power: float):
        await interaction.response.send_message(num**power)


async def setup(bot):
    await bot.add_cog(Math(bot=bot))
