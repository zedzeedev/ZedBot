import discord


class StartMenu(discord.ui.View):
    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.match_accepted = False
