import discord
from discord.ext import commands
from discord import app_commands
from menus.game_menus.black_jack_menus import StartMenu


class BlackJack(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @app_commands.command(name="blackjack-play", description="Starts a game of Black Jack")
    async def black_jack_play(self, interaction: discord.Interaction, user: discord.User):
        start_menu = StartMenu(player1=interaction.user, player2=user, ctx=interaction)

        embed = start_menu.create_embed()
        await interaction.response.send_message("Sending message...", ephemeral=True)
        await interaction.followup.send(embed=embed, view=start_menu)


async def setup(bot):
    await bot.add_cog(BlackJack(bot=bot))
