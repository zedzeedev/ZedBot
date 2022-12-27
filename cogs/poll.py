import discord
from discord.ext import commands
from discord import app_commands
from menus.pollmenu import PollMenu


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(description="Creates a poll.")
    
    @app_commands.describe(
        title="The title of the poll",
        description="The description/body of the poll",
        options="The options in the poll, format: Option1,Option2,Option3...."
    )
    
    async def poll(self, interaction: discord.Interaction, title: str, description: str, options: str):
        opts = options.split(sep=',')
        for opt in opts:
            opt = opt.replace(',', ' ')

        poll = PollMenu(title=title, options=opts, description=description)
        embed = poll.create_embed()

        await interaction.response.send_message(embed=embed, view=poll)


async def setup(bot):
    await bot.add_cog(Poll(bot=bot))
