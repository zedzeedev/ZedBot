import discord
import json
from random import choices
from string import ascii_letters, digits


bot = discord.Bot()

with open("config.json") as conf:
    config = json.load(fp=conf)


class PollMenu(discord.ui.View):
    def __init__(self, options, title, description):
        super().__init__()

        self.voted = []
        self.options = []
        self.embed = None
        self.description = description
        self.title = title
        for opt in options:
            self.options.append({"option": opt, "votes": 0})
        self.option_buttons = []
        for option in self.options:
            self.option_buttons.append(discord.ui.Button(label=option["option"], style=discord.ButtonStyle.gray, custom_id="".join(choices(ascii_letters + digits, k=20))))
        for button in self.option_buttons:
            button.callback = self.__on_button_callback
            self.add_item(button)

    
    async def __on_button_callback(self, interaction: discord.Interaction):
        for button in self.option_buttons:
            if interaction.data["custom_id"] == button.custom_id:
                current = self.option_buttons.index(button)
        
        current_option = self.options[current]

        if interaction.user in self.voted:
            await interaction.response.send_message("You already voted!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You have voted for {current_option['option']}", ephemeral=True)
            current_option['votes'] += 1
            self.voted.append(interaction.user)
            await interaction.message.edit(embed=self.create_embed())
    
    def create_embed(self):
        self.description = ""
        
        self.embed = discord.Embed(color=discord.colour.Color.random(), title=self.title, description=self.description)
        for option in self.options:
            self.embed.add_field(name=option["option"], value=f"{option['option']}, Voted: {option['votes']}", inline=False)
        return self.embed


@bot.event
async def on_ready():
    pass


@bot.event
async def on_message(message):
    pass


@bot.command()
async def lesbian(ctx):
    await ctx.respond("yeah, thats me")


@bot.command(description="Forces the bot to send the given message.")
async def talk(ctx, msg: str):
    await ctx.respond("Message sending...", ephemeral=True)
    await ctx.send(msg)


@bot.command(description="WARNING: DO NOT USE")
async def avery(ctx):
    for i in range(0, 100):
        await ctx.respond("omg thats so fucking hot")


cogs_list = [
    "math",
    "bomb_tag",
    "poll"
]


for cog in cogs_list:
    bot.load_extension(f"cogs.{cog}")


bot.run(config["token"])
