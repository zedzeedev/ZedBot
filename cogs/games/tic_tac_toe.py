import discord
from discord.ext import commands
from discord import app_commands
from menus.game_menus.tic_tac_toe_menus import StartMenu


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @app_commands.command(name="tictactoe-play", description="Starts a game of Tic-Tac-Toe")
    async def tic_tac_toe_play(self, interaction: discord.Interaction, user: discord.User):
        start_menu = StartMenu({"plr": interaction.user, "color": "❌"}, {"plr": user, "color": "⭕"})
        
        embed = start_menu.create_embed()
        await interaction.response.send_message("Sending message...", ephemeral=True)
        await interaction.followup.send(embed=embed, view=start_menu)


async def setup(bot):
    await bot.add_cog(TicTacToe(bot=bot))
