import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image
from string import ascii_letters, digits
import random


class DiscordPlace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="place-pixel", description="Places a pixel on the canvas")
    @app_commands.choices(color=[
        app_commands.Choice(name="red", value=0),
        app_commands.Choice(name="blue", value=1),
        app_commands.Choice(name="green", value=2)
    ])
    async def place_pixel(self, interaction: discord.Interaction, ctx, x: int, y: int, colors: app_commands.Choice[int]):
        color = (0, 0, 0)
        
        if colors.value == 0:
            color = (255, 0, 0)
        if colors.value == 1:
            color = (0, 0, 255)
        if colors.value == 2:
            color = (0, 255, 0)
        
        canvas = Image.open("dplace/canvas.png")

        if x >= canvas.size[0] or y >= canvas.size[1]:
            await interaction.response.send_message("The position is invalid!", ephemeral=True)
        
        canvas.putpixel((x, y), color)
        canvas.save("dplace/canvas.png")
        
        # Create the embed 
        embed = discord.Embed(title="Canvas", description="Testing!")
        embed.set_image(url="dplace/canvas.png")
        
        await interaction.response.send_message("Done!", embed=embed)
    
    @app_commands.command(name="crop-canvas")
    @app_commands.describe(
        left="The left coordinate of the box to crop, must be less than `right`",
        top="The top coordinate of the box to crop, must be less than `bottom`",
        right="The right coordinate of the box to crop, must be more than `left`",
        bottom="The bottom coordinate of the box to crop, must be more than `top`"
    )
    async def crop_canvas(self, interaction: discord.Interaction, ctx, 
                          left: int, top: int, right: int, bottom: int):
        if left > right or top > bottom:
            await interaction.response.send_message("Invalid box coordinates!", ephemeral=True)
        
        canvas = Image.open("dplace/canvas.png")
        
        if right >= canvas.size[0] or bottom > canvas.size[1]:
            await interaction.response.send_message("Invalid box coordinates!", ephemeral=True)
        
        cropped = canvas.crop((left, top, right, bottom))
        code = "".join(random.choices(ascii_letters + digits, k=20))
        name = f"crop_{code}"
        cropped.save(f"{name}.png")
        
        # Create the embed
        embed = discord.Embed(title="Cropped Canvas", description="Testing!")
        embed.set_image(url=f"{name}.png")
        
        await interaction.response.send_message("Done!", embed=embed)
        
    
    
def setup(bot):
    bot.add_cog(DiscordPlace(bot))
