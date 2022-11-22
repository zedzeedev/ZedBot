import discord
from menus.game_menus.helpers.game_menus import TwoPlayerMenu
from menus.game_menus.helpers.board import Board
import random
import string


class StartMenu(discord.ui.View):
    def __init__(self, player1: discord.User, player2: discord.User):
        super().__init__()
        self.x_player = player1
        self.o_player = player2
        self.match_accepted = False
    
    def create_embed(self):
        embed = discord.Embed(title="Connect Four", description=f"{self.x_player['plr']} would like to play Tic-Tac-Toe with {self.o_player['plr']}")

        return embed
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept_button_callback(self, button, interaction: discord.Interaction):
        if self.__is_second_player(interaction.user) and not self.match_accepted:
            self.match_accepted = True
            game_menu = TicTacToeGame(self.x_player, self.o_player)
            await interaction.response.send_message(embed=game_menu.create_embed(), view=game_menu)
        elif self.match_accepted:
            await interaction.response.send_message(f"This match has already started!")
        else:
            await interaction.response.send_message(f"You are not the requested user!", ephemeral=True)
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline_button_callback(self, button, interaction: discord.Interaction):
        if self.__is_second_player(interaction.user):
            self.match_accepted = False
            await interaction.response.send_message(f"{self.o_player['plr']} has declined your TicTacToe request!")
        else:
            await interaction.response.send_message(f"You are not the requested user!")
            
    def __is_second_player(self, plr: discord.User):
        return plr == self.o_player["plr"]
    

class TicTacToeGame(TwoPlayerMenu):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.board = Board(x=3, x=3, num_to_match=3)
        
        for row in range(1, 8):
            self.buttons.append(discord.ui.Button(
                label=row, style=discord.ButtonStyle.gray, 
                custom_id=''.join(random.choices(string.ascii_letters + string.digits, k=20))))
            
        for button in self.buttons:
            button.callback = self.button_callback_event
            self.add_item(button)
    
    async def button_callback_event(self, interaction: discord.Interaction):
        current = self.find_index_from_id(interaction.data["custom_id"])
        
        if self.winner == None:
            await interaction.response.send_message(current + 1, ephemeral=True)
            follow_up = interaction.followup
