import discord
from discord.ext import commands
from menus.game_menus.black_jack_menus import StartMenu


class BlackJack(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @discord.slash_command(name="blackjack-play", description="Starts a game of Black Jack")
    async def black_jack_play(self, ctx, user: discord.User):
        start_menu = StartMenu(player1=ctx.author, player2=user)
        
        embed = start_menu.create_embed()
        await ctx.respond("Sending message...", ephemeral=True)
        await ctx.send(embed=embed, view=start_menu)


def setup(bot):
    bot.add_cog(BlackJack(bot=bot))
