import discord
from discord.ext import commands
from menus.bomb_tag_menus import StartMenu


class BombTag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_running = False
    
    @discord.slash_command(description="Starts a game of bomb tag.")
    async def start(self, ctx, character: str):
        if not self.game_running:
            self.game_running = True
            creator = {"creator": ctx.author, "character": character}
            start_menu = StartMenu(creator=creator)
            
            await ctx.respond("Starting game...", ephemeral=True)
            await ctx.respond(embed=start_menu.create_embed(), view=start_menu)
        else:
            await ctx.respond("There is already a game running!")
        

def setup(bot):
    bot.add_cog(BombTag(bot=bot))
