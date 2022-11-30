import discord
from discord.ext import commands
from menus.game_menus.connect_four_menus import StartMenu


class ConnectFour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.slash_command(name="connect4-play", description="Starts a game of connect4")
    async def connectfour_play(self, ctx, user: discord.User):
        start_menu = StartMenu(player1={"plr": ctx.author, "color": "🟥"}, player2={"plr": user, "color": "🟨"})
        
        embed = start_menu.create_embed()
        await ctx.respond("Sending message...", ephemeral=True)
        await ctx.send(embed=embed, view=start_menu)


def setup(bot):
    bot.add_cog(ConnectFour(bot=bot))
    