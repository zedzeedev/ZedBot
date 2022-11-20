import discord
from discord.ext import commands
from menus.game_menus.gomoku_menus import StartMenu


class Gomoku(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @discord.slash_command(name="gomoku-play", description="Starts a game of Gomoku")
    async def gomoku_play(self, ctx, user: discord.User):
        start_menu = StartMenu(player1={"plr": ctx.author, "color": "🟥"}, player2={"plr": user, "color": "🟨"})
        
        embed = start_menu.create_embed()
        await ctx.respond("Sending message...", ephemeral=True)
        await ctx.send(embed=embed, view=start_menu)


def setup(bot):
    bot.add_cog(Gomoku(bot=bot))
    