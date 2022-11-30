import discord
from menus.game_menus.helpers.cards import Card, deal_cards, add_card, random_card, deal_deck, sum_of_deck
from menus.game_menus.helpers.game_menus import TwoPlayerMenu


class StartMenu(discord.ui.View):
    def __init__(self, player1: discord.User, player2: discord.User):
        super().__init__()
        self.player1 = player1
        self.player2 = player2
        self.match_accepted = False
    
    def create_embed(self):
        embed = discord.Embed(title="Connect Four", description=f"{self.x_player['plr']} would like to play Tic-Tac-Toe with {self.o_player['plr']}")

        return embed
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept_button_callback(self, button, interaction: discord.Interaction):
        if self.__is_second_player(interaction.user) and not self.match_accepted:
            self.match_accepted = True
            game_menu = BlackJackGame(self.player1, self.player2)
            await interaction.response.send_message(embed=game_menu.create_embed(), view=game_menu)
        elif self.match_accepted:
            await interaction.response.send_message(f"This match has already started!")
        else:
            await interaction.response.send_message(f"You are not the requested user!", ephemeral=True)
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline_button_callback(self, button, interaction: discord.Interaction):
        if self.__is_second_player(interaction.user):
            self.match_accepted = False
            await interaction.response.send_message(f"{self.player2['plr']} has declined your TicTacToe request!")
        else:
            await interaction.response.send_message(f"You are not the requested user!")
            
    def __is_second_player(self, plr: discord.User):
        return plr == self.player2["plr"]
    
    
def change_value(card):
    if card.number == 1:
        card.number = 11
    elif card.number > 10:
        card.number = 10


# Used to modify cards for blackjack
def change_values(decks):
    for deck in decks:
        for i, val, in enumerate(deck["cards"]):
            deck[i] = change_value(val)


class BlackJackGame(TwoPlayerMenu):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.player1 = {"plr": player1, "deck": deal_deck(2), "stay": False}
        self.player2 = {"plr": player2, "deck": deal_deck(2), "stay": False}
        
        if sum_of_deck(player1) == 21:
            self.winner = player1
        if sum_of_deck(player2) == 21:
            self.winner = player2
    
    def create_embed(self):
        pass
    
    @discord.ui.button(label="Hit")
    async def hit_button_callback(self, button, interaction: discord.Interaction):
        if self.winner == None:
            
            if interaction.user == self.current_player["plr"]:
                add_card(self.current_player["deck"], change_value(random_card()))
                self.current_player["stay"] = False
                
                sum = sum_of_deck(self.current_player["deck"])
                if sum == 21:
                    self.winner = self.current_player
                elif sum > 21:
                    self.winner = self.other_player
                self.current_player, self.other_player = self.other_player, self.current_player
            else:
                await interaction.response.send_message("You are not the requested user!", ephemeral=True)
        else:
            await interaction.response.send_message(f"{self.winner['plr']} has already won the game!")
    
    @discord.ui.button(label="Stand")
    async def stand_button_callback(self, button, interaction: discord.Interaction):
        if self.winner == None:
            
            if interaction.user == self.current_player["plr"]:
                self.current_player["stay"] == True
                
                if self.other_player["stay"]:
                    sum = sum_of_deck(self.current_player["deck"])
                    sum_plr2 = sum_of_deck(self.other_player["deck"])
                    
                    if sum > sum_plr2:
                        self.winner = self.current_player
                    else:
                        self.winner = self.other_player
                        
                self.current_player, self.other_player = self.other_player, self.current_player
           
                