import discord
from random import choices
from string import ascii_letters, digits


class PollMenu(discord.ui.View):
    def __init__(self, options, title, description):
        super().__init__()
        self.voted = []
        self.options = []
        self.description = description
        self.title = title
        
        for opt in options:
            self.options.append({"option": opt, "votes": 0})
            
        self.option_buttons = []
        for option in self.options:
            self.option_buttons.append(discord.ui.Button(label=option["option"], style=discord.ButtonStyle.gray, custom_id="".join(choices(ascii_letters + digits, k=20))))
        
        for button in self.option_buttons:
            button.callback = self.on_button_callback
            self.add_item(button)

    def create_embed(self):
        embed = discord.Embed(color=discord.colour.Color.random(), title=self.title, description=self.description)
        
        for option in self.options:
            embed.add_field(name=option["option"], value=f"{option['option']}, Voted: {option['votes']}", inline=False)
        return embed

    async def on_button_callback(self, interaction: discord.Interaction):
        current = self.__find_index_from_id(interaction.data["custom_id"])
        # Uses the set custom ID of the button to get the index of its position
        
        current_option = self.options[current]

        if self.__voter_exists(interaction.user):
            current_option["votes"] += 1
            old_option = self.options[self.__find_voter(interaction.user)["chosen"]]
            old_option["votes"] -= 1
            self.__find_voter(interaction.user)["chosen"] = current
            await interaction.response.send_message(f"You have changed your vote to {current_option['option']}", ephemeral=True)
        else:
            await interaction.response.send_message(f"You have voted for {current_option['option']}", ephemeral=True)
            current_option["votes"] += 1
            self.voted.append({"user": interaction.user, "chosen": current})

        await interaction.message.edit(embed=self.create_embed())

    def __voter_exists(self, user):
        for voter in self.voted:
            if voter["user"] == user:
                return True
        return False
    
    def __find_voter(self, user):
        for voter in self.voted:
            if voter["user"] == user:
                return voter
        return user

    def __find_index_from_id(self, id):
        for i, button in enumerate(self.option_buttons):
            if button.custom_id == id:
                return i
        return 0
