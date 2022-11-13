import discord
from discord.ext import commands


class BombTag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_running = False
        self.players = []
        self.creator = None
    
    @discord.slash_command(description="Starts a game of bomb tag.")
    async def start(self, ctx):
        if not self.game_running:
            self.game_running = True
            self.creator = ctx.author
        else:
            await ctx.respond("There is already a game running!")
    
    @discord.slash_command(description="Joins the on-going game!")
    async def join(self, ctx):
        self.players.append(ctx.author)
    
    @discord.slash_command(description="Starts the match of bomb tag!")
    async def start_match(self, ctx):
        if ctx.author != self.author:
            await ctx.respond("You did not create this game of bomb tag!", ephemeral=True)
        else:
            pass
    
        

def setup(bot):
    bot.add_cog(BombTag(bot=bot))
