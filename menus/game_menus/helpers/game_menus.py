import discord
from abc import ABC, abstractmethod


class TwoPlayerMenu(discord.ui.View, ABC):
    def __init__(self, player1, player2):
        super().__init__()
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.other_player = player2
        self.winner = None
        self.buttons = []
        
    def find_index_from_id(self, id):
        for i, button in enumerate(self.buttons):
            if button.custom_id == id:
                return i
        return 0
    
    async def button_callback_event(self, interaction: discord.Interaction):
        pass
