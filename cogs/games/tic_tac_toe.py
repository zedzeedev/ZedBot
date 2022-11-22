import discord
from discord.ext import commands
from menus.game_menus.tic_tac_toe_menus import StartMenu


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @discord.slash_command(name="tictactoe-play", description="Starts a game of Tic-Tac-Toe")
    async def tic_tac_toe_play(self, ctx, user: discord.User):
        start_menu = StartMenu({"plr": ctx.author, "symbol": "❌"}, {"plr": user, "symbol": "⭕"})
        
        embed = start_menu.create_embed()
        await ctx.respond("Sending message...", ephemeral=True)
        await ctx.send(embed=embed, view=start_menu)


def setup(bot):
    bot.add_cog(TicTacToe(bot=bot))
