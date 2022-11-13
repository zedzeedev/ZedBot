import discord
from discord.ext import commands
from string import ascii_lowercase
import random


class BombTag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_running = False
        self.players = []
        self.creator = []
        self.match_started = False
    
    @discord.slash_command(description="Starts a game of bomb tag.")
    async def start(self, ctx, character: str):
        if not self.game_running:
            self.game_running = True
            self.creator.append(ctx.author)
            self.creator.append(character[0])
            
            view = discord.ui.View()
            join_button = discord.ui.Button(style=discord.ButtonStyle.green, label="Join Game")
            start_match_button = discord.ui.Button(style=discord.ButtonStyle.green, label="Start Match")
            
            
            async def join_button_callback(interaction: discord.Interaction):
                if not self.__plr_exists(interaction.user) and interaction.user != self.creator[0]:
                    char = random.choice(ascii_lowercase)
                    while self.__char_exists(char):
                        char = random.choice(ascii_lowercase)
                    
                    self.players.append({"player": interaction.user, "character": char})
                    await interaction.response.send_message(f"You have joined the game! Your character is {char}", ephemeral=True)
                else:
                    await interaction.response.send_message("You are already in the match!", ephemeral=True)
            
            
            async def start_match_callback(interaction: discord.Interaction):
                if not self.match_started:
                    if interaction.user == self.creator[0]:
                        await interaction.response.send_message("The match is starting...")
                        self.match_started = True
                    else:
                        await interaction.response.send_message("You did not create this match!", ephemeral=True)
                else:
                    await interaction.response.send_message("The match is already started!", ephemeral=True)
            
            
            start_match_button.callback = start_match_callback
            join_button.callback = join_button_callback
            view.add_item(join_button)
            view.add_item(start_match_button)
            embed = discord.Embed(title="Bomb Tag", description="Dont let the timer run out while holding the bomb!")
            await ctx.respond("Starting game...", ephemeral=True)
            await ctx.respond(embed=embed, view=view)
        else:
            await ctx.respond("There is already a game running!")
        
    def __plr_exists(self, user):
        for plr in self.players:
            if plr["player"] == user:
                return True
        return False
    
    def __char_exists(self, char):
        for plr in self.players:
            if plr["character"] == char:
                return True
        return False
        

def setup(bot):
    bot.add_cog(BombTag(bot=bot))
