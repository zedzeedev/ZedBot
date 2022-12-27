import discord
from discord.ext import commands
from discord import app_commands
from menus.game_menus.connect_four_menus import StartMenu


class ConnectFour(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @app_commands.command(name="connect4-play", description="Starts a game of connect4")
    async def connectfour_play(self, interaction: discord.Interaction, user: discord.User):
        start_menu = StartMenu(player1={"plr": interaction.user, "color": "🟥"}, player2={"plr": user, "color": "🟨"})
        
        embed = start_menu.create_embed()
        await interaction.response.send_message("Sending message...", ephemeral=True)
        followup = interaction.followup
        await followup.send(embed=embed, view=start_menu)


async def setup(bot):
    await bot.add_cog(ConnectFour(bot=bot))
    