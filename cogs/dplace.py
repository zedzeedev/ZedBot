import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image
from string import ascii_letters, digits
import random
import os


class DiscordPlace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="place-pixel", description="Places a pixel on the canvas")
    @app_commands.choices(colors=[
        app_commands.Choice(name="red", value=0),
        app_commands.Choice(name="blue", value=1),
        app_commands.Choice(name="green", value=2)
    ])
    async def place_pixel(self, interaction: discord.Interaction, x: int, y: int, colors: app_commands.Choice[int]):
        color = (0, 0, 0)
        
        if colors.value == 0:
            color = (255, 0, 0)
        if colors.value == 1:
            color = (0, 0, 255)
        if colors.value == 2:
            color = (0, 255, 0)
        
        canvas = Image.open("cogs/dplace/canvas.png")

        if x > canvas.size[0] or y > canvas.size[1] or x < 0 or y < 0:
            await interaction.response.send_message("The position is invalid!", ephemeral=True)
            return
        
        canvas.putpixel((x, y), color)
        canvas.save("cogs/dplace/canvas.png")
        
        # Create the embed 
        f = discord.File("cogs/dplace/canvas.png", filename="canvas.png")
        embed = discord.Embed(title="Canvas", description="Testing!")
        embed.set_image(url="attachment://canvas.png")
        
        await interaction.response.send_message("Done!", embed=embed, file=f)
    
    @app_commands.command(name="crop-canvas")
    @app_commands.describe(
        left="The left coordinate of the box to crop, must be less than `right`",
        top="The top coordinate of the box to crop, must be less than `bottom`",
        right="The right coordinate of the box to crop, must be more than `left`",
        bottom="The bottom coordinate of the box to crop, must be more than `top`"
    )
    async def crop_canvas(self, interaction: discord.Interaction, 
                          left: int, top: int, right: int, bottom: int):
        if left > right or top > bottom:
            await interaction.response.send_message("Invalid box coordinates!", ephemeral=True)
            return
        
        canvas = Image.open("cogs/dplace/canvas.png")
        
        if right > canvas.size[0] or bottom > canvas.size[1]:
            await interaction.response.send_message("Invalid box coordinates!", ephemeral=True)
            return
        
        cropped = canvas.crop((left, top, right, bottom))
        code = "".join(random.choices(ascii_letters + digits, k=20))
        name = f"crop_{code}"
        cropped.save(f"cogs/dplace/crops/{name}.png")
        
        # Create the embed
        f = discord.File(f"cogs/dplace/crops/{name}.png", filename="new_crop.png")
        embed = discord.Embed(title="Cropped Canvas", description="Testing!")
        embed.set_image(url=f"attachment://new_crop.png")
        
        await interaction.response.send_message("Done!", embed=embed, file=f)
    
    def _resize_no_filter(img: Image.Image, new_size: tuple[int, int]) -> Image.Image:
        width, height = img.size
        ratio_width = new_size[0] // width
        ratio_height = new_size[1] // height

        pixels = {}

        for row in range(width):
            for col in range(height):
                pixels[(row, col)] = img.getpixel((row, col))

        new_img = Image.new("RGBA", new_size)

        for row in range(new_size[0]):
            for col in range(new_size[1]):
                new_img.putpixel((row, col), pixels[row // ratio_width, col // ratio_height])
                
        return new_img


async def setup(bot):
    await bot.add_cog(DiscordPlace(bot=bot))
