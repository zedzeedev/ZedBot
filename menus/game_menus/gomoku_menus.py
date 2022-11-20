import discord
from menus.game_menus.helpers.board import Board, Cell
from string import ascii_letters, digits
import random
from menus.game_menus.helpers.game_menus import TwoPlayerMenu


class StartMenu(discord.ui.View):
    def __init__(self, player1: discord.User, player2: discord.User):
        super().__init__()
        self.red_player = player1
        self.yellow_player = player2
        self.match_accepted = False
    
    def create_embed(self):
        embed = discord.Embed(title="Connect Four", description=f"{self.red_player['plr']} would like to play Gomoku with {self.yellow_player['plr']}")

        return embed
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept_button_callback(self, button, interaction: discord.Interaction):
        if self.__is_second_player(interaction.user) and not self.match_accepted:
            self.match_accepted = True
            game_menu = GomokuGame(self.red_player, self.yellow_player)
            
            await interaction.response.send_message(embed=game_menu.create_embed(), view=game_menu)
        elif self.match_accepted:
            await interaction.response.send_message(f"This match has already started!")
        else:
            await interaction.response.send_message(f"You are not the requested user!", ephemeral=True)
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline_button_callback(self, button, interaction: discord.Interaction):
        if self.__is_second_player(interaction.user):
            self.match_accepted = False
            await interaction.response.send_message(f"{self.yellow_player['plr']} has declined your Gomoku request!")
        else:
            await interaction.response.send_message(f"You are not the requested user!")
            
    def __is_second_player(self, plr: discord.User):
        return plr == self.yellow_player["plr"]
    

class GomokuGame(TwoPlayerMenu):
    def __init__(self, player1, player2):
        super().__init__(player1=player1, player2=player2)
        self.board = Board(x=15, y=15, num_to_match=5)
        for row in range(1, 16):
            self.buttons.append(discord.ui.Button(
                label=row, style=discord.ButtonStyle.gray, 
                custom_id=''.join(random.choices(ascii_letters + digits, k=20))))
        self.turns = 0
        self.current_row = 0
        self.current_col = 0
        
        for button in self.buttons:
            button.callback = self.button_callback_event
            self.add_item(button)
        
    def create_embed(self):
        embed = discord.Embed(title="Gomoku", description=self.board.reverse_str())
        embed.set_footer(text=f"It is {self.current_player['plr']}'s turn.")
        
        if self.winner != None:
            embed.remove_footer()
            embed.add_field(name="Winner!", value=f"{self.winner['plr']} {self.winner['color']} has won the game of Connect Four!")
        return embed
    
    async def button_callback_event(self, interaction: discord.Interaction):
        current = self.find_index_from_id(interaction.data["custom_id"])
        
        if self.winner == None:
            await interaction.response.send_message(current + 1, ephemeral=True)
            follow_up = interaction.followup
            
            if interaction.user == self.current_player["plr"]:
                self.turns += 1
                if self.turns == 1:
                    self.current_row = current
                else:
                    self.current_col = current
            
                if self.turns > 2:
                    if self.board[self.current_row, self.current_col]["taken"]:
                        self.turns = 0
                    else:
                        self.board[self.current_row, self.current_col] = Cell(self.current_player["color"], True)
                        self.current_col = 0
                        self.current_row = 0
                        
                        if self.board.winner:
                            self.winner = self.current_player
                            await interaction.message.edit(embed=self.create_embed())
                        self.current_player, self.other_player = self.other_player, self.current_player

                    
                await interaction.message.edit(embed=self.create_embed())
            elif interaction.user == self.other_player["plr"]:
                await follow_up.send("It is not your turn yet!", ephemeral=True)
            else:
                await follow_up.send("You are not a part of this game!", ephemeral=True)       
            
        else:
            await interaction.response.send_message(f"{self.winner['plr']} already won!", ephemeral=True)

        