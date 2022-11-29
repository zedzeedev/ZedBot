import discord
from menus.game_menus.helpers.cards import Card, deal_cards, add_card, random_card, deal_deck
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
    

# Used to modify cards
def change_values(decks):
    for deck in decks:
        for i, val, in enumerate(deck["cards"]):
            if val.number == 1:
                deck["cards"][i] = Card().add_number(11).add_suite(val.suite).add_color(val.color)
            elif val.number > 10:
                deck["cards"][i] = Card().add_number(10).add_suite(val.suite).add_color(val.color)


def change_value(card):
    if card.number == 1:
        card.number = 11
    elif card.number > 10:
        card.number = 10


class BlackJackGame(TwoPlayerMenu):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.player1 = {"plr": player1, "deck": deal_deck(2)}
        self.player2 = {"plr": player2, "deck": deal_deck(2)}
        
    @discord.ui.button(label="Hit")
    async def hit_button_callback(self, button, interaction: discord.Interaction):
        pass
    
    @discord.ui.button(label="Stand")
    async def stand_button_callback(self, button, interaction: discord.Interaction):
        pass
