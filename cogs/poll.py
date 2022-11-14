import discord
from discord.ext import commands
from random import choices
from string import ascii_letters, digits
from bot import PollMenu


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(description="Creates a poll. Format for options: Option1,Option2,Option3")
    async def poll(self, ctx, title: str, description: str, options: str):
        opts = options.split(sep=',')
        for opt in opts:
            opt = opt.replace(',', ' ')

        poll = PollMenu(title=title, options=opts, description=description)
        embed = poll.create_embed()

        await ctx.respond(embed=embed, view=poll)


def setup(bot):
    bot.add_cog(Poll(bot=bot))
