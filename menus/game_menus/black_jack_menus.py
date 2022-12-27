import discord
from menus.game_menus.helpers.cards import Card, deal_cards, add_card, random_card, deal_deck, sum_of_deck
from menus.game_menus.helpers.game_menus import TwoPlayerMenu


def change_value(card):
    if card.number == 1:
        card.number = 11
    elif card.number > 10:
        card.number = 10
    return card


# Used to modify cards for blackjack
def change_values(deck):
    for i, val, in enumerate(deck):
        deck[i] = change_value(val)
    return deck


def create_cards_embed(player):
    descr = ""
        
    for card in player["deck"]:
        descr += str(f"{card}\n")
    descr += f"Amount: {sum_of_deck(player['deck'])}"
    return discord.Embed(title="Cards:", description=descr)


class StartMenu(discord.ui.View):
    def __init__(self, player1: discord.User, player2: discord.User, ctx):
        super().__init__()
        self.player1 = {"plr": player1, "deck": change_values(deal_deck(2)), "stay": False}
        self.player2 = {"plr": player2, "deck": change_values(deal_deck(2)), "stay": False}
        self.ctx = ctx.followup
        self.match_accepted = False
    
    def create_embed(self):
        embed = discord.Embed(title="BlackJack", description=f"{self.player1['plr']} would like to play BlackJack with {self.player2['plr']}")

        return embed
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept_button_callback(self, interaction: discord.Button, button: discord.Button):
        if self.__is_second_player(interaction.user) and not self.match_accepted:
            self.match_accepted = True
            
            game_menu = BlackJackGame(self.player1, self.player2)
            
            await interaction.response.send_message(embed=game_menu.create_embed(), view=game_menu)
            follow_up = interaction.followup
            
            await follow_up.send(embed=create_cards_embed(self.player2), ephemeral=True)
            await self.ctx.send(embed=create_cards_embed(self.player1), ephemeral=True)
            
        elif self.match_accepted:
            await interaction.response.send_message(f"This match has already started!")
        else:
            await interaction.response.send_message(f"You are not the requested user!", ephemeral=True)
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline_button_callback(self, interaction: discord.Interaction, button: discord.Button):
        if self.__is_second_player(interaction.user):
            self.match_accepted = False
            await interaction.response.send_message(f"{self.player2['plr']} has declined your BlackJack request!")
        else:
            await interaction.response.send_message(f"You are not the requested user!")
                
    def __is_second_player(self, plr: discord.User):
        return plr == self.player2["plr"]
    

class BlackJackGame(TwoPlayerMenu):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        
        if sum_of_deck(self.player1["deck"]) == 21:
            self.winner = self.player1
        if sum_of_deck(self.player2["deck"]) == 21:
            self.winner = self.player2
    
    def create_embed(self):
        embed = discord.Embed(title="BlackJack", description="")
        desc = ""
        
        # Add a emoji for each one of the first players cards
        
        for _ in self.player1["deck"]:
            desc += "🟥"
        
        # Check if there was a bust
            
        deck_sum = sum_of_deck(self.player1["deck"])
        
        if deck_sum > 21:
            desc += "\nBust!"
        else:
            desc += f"\nStanding: {self.player1['stay']}"
        
        embed.add_field(name=f"{self.player1['plr']}", value=desc)
        
        
        desc = ""
        
        # Add an emoji for each one of the second players cards
        
        for _ in self.player2["deck"]:
            desc += "⬜"

        deck_sum = sum_of_deck(self.player2["deck"])
        
        if deck_sum > 21:
            desc += "\nBust!"
        else:
            desc += f"\nStanding: {self.player2['stay']}"
        
        embed.add_field(name=f"{self.player2['plr']}", value=desc)
        
        embed.set_footer(text=f"It is {self.current_player['plr']}'s turn.")
        
        if self.winner != None:
            embed.remove_footer()
            embed.add_field(name="Winner!", value=f"{self.winner['plr']} has won the game of BlackJack")
        return embed
    
    @discord.ui.button(label="Hit")
    async def hit_button_callback(self, button, interaction: discord.Interaction):
        if self.winner == None:
            
            if interaction.user == self.current_player["plr"]:                
                add_card(self.current_player["deck"], change_value(random_card()))
                self.current_player["stay"] = False
                
                await interaction.response.send_message(embed=create_cards_embed(self.current_player), ephemeral=True)
                
                sum = sum_of_deck(self.current_player["deck"])
                if sum == 21:
                    self.winner = self.current_player
                elif sum > 21:
                    self.winner = self.other_player
                self.current_player, self.other_player = self.other_player, self.current_player
                await interaction.message.edit(embed=self.create_embed())
            else:
                await interaction.response.send_message("You are not the requested user!", ephemeral=True)
        else:
            await interaction.response.send_message(f"{self.winner['plr']} has already won the game!", ephemeral=True)
    
    @discord.ui.button(label="Stand")
    async def stand_button_callback(self, button, interaction: discord.Interaction):
        if self.winner == None:
            
            if interaction.user == self.current_player["plr"]:
                self.current_player["stay"] = True
                
                if self.other_player["stay"]:
                    sum = sum_of_deck(self.current_player["deck"])
                    sum_plr2 = sum_of_deck(self.other_player["deck"])
                    
                    if sum > sum_plr2:
                        self.winner = self.current_player
                    else:
                        self.winner = self.other_player
                
                await interaction.response.send_message(embed=create_cards_embed(self.current_player), ephemeral=True)
                        
                self.current_player, self.other_player = self.other_player, self.current_player
                await interaction.message.edit(embed=self.create_embed())
           