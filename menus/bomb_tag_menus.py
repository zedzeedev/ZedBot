import discord
import random
from string import ascii_lowercase


class StartMenu(discord.ui.View):
    def __init__(self, creator):
        super().__init__()
        self.players = []
        self.creator = creator
        self.match_started = False

    @discord.ui.button(label="Join game")
    async def __join_button_callback(self, button, interaction: discord.Interaction):
        if self.__plr_exists(interaction.user) or interaction.user == self.creator["creator"]:
            await interaction.response.send_message("You are already in the match!")
        else:
            char = random.choice(ascii_lowercase)
            while self.__char_exists(char):
                char = random.choice(ascii_lowercase)
            
            self.players.append({"player": interaction.user, "character": char})
            await interaction.response.send_message(f"You have joined the game! Your character is {char}", ephemeral=True)

    @discord.ui.button(label="Start match")
    async def __start_match_callback(self, button, interaction: discord.Interaction):
        if interaction.user == self.creator['user']:
            interaction.response.send_message("Starting game...")
            self.match_started = True
        else:
            interaction.response.send_message("You did not create the match!")
            
    def create_embed(self):
        return discord.Embed(title="Bomb Tag", description="Dont let the timer run out while holding the bomb!")
    
    def __plr_exists(self, player):
        for plr in self.players:
            if plr["player"] == player:
                return True
        return False
    
    def __char_exists(self, char):
        for plr in self.players:
            if plr["character"] == char:
                return True
        return False