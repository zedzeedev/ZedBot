import discord
from discord.ext import commands
from random import choices
from string import ascii_letters, digits


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voted = []
        self.options = []
        self.title = ""
        self.embed = None
    
    @discord.slash_command(description="Creates a poll. Format for options: Option1,Option2,Option3")
    async def poll(self, ctx, title: str, options: str):
        self.embed = None
        self.voted = []
        self.options = []
        self.title = ""
        self.title = title

        opts = options.split(sep=',')
        for opt in opts:
            opt = opt.replace(',', ' ')

        for option in opts:
            self.options.append({
                "option": option,
                "votes": 0
            })

        description = ""

        for option in self.options:
            description += f"{option['option']}, Votes: {option['votes']}\n"

        self.embed = discord.Embed(title=title, description=description, color=discord.colour.Color.random())
        await ctx.respond("Creating poll", ephemeral=True)
        await ctx.send(embed=self.embed, view=self.__create_view())
    
    def __create_view(self) -> discord.ui.View:
        view = discord.ui.View()
        option_buttons = []
        for option in self.options:
            option_buttons.append(discord.ui.Button(style=discord.ButtonStyle.gray, label=option["option"], custom_id="".join(choices(ascii_letters + digits, k=20))))


        async def option_callback(interaction: discord.Interaction):
            for button in option_buttons:
                if interaction.data["custom_id"] == button.custom_id:
                    current = option_buttons.index(button)

            current_option = self.options[current]

            if interaction.user in self.voted:
                await interaction.response.send_message("You already voted!", ephemeral=True)
            else:
                await interaction.response.send_message(f"You have voted for {current_option['option']}", ephemeral=True)
                current_option['votes'] += 1
                self.voted.append(interaction.user)
                self.embed = discord.Embed(title=self.title, description=self.__refresh_message(), color=discord.colour.Color.random())
                await interaction.message.edit(embed=discord.Embed(title=self.title, description=self.__refresh_message(), color=discord.colour.Color.random()))

        
        for button in option_buttons:
            button.callback = option_callback
            

        for button in option_buttons:
            view.add_item(button)


        return view
    
    def __refresh_message(self):
        description = ""

        for option in self.options:
            description += f"{option['option']}, Votes: {option['votes']}\n"
        
        return description



def setup(bot):
    bot.add_cog(Poll(bot=bot))
