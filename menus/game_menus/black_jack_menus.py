import discord


class StartMenu(discord.ui.View):
    def __init__(self, player1):
        super().__init__()
        self.creator = player1
        self.players = [player1]

    def create_embed(self) -> discord.Embed:
        embed = discord.Embed(title="Black Jack")
        embed.add_field(name="Creator: ", value=self.creator, inline=True)
        s = ""
        for player in self.players:
            s += player
        embed.add_field(name="Players:", value=s, inline=False)
        
        return embed
    
    @discord.ui.button(label="Join")
    async def join_button_callback(self, button, interaction: discord.Interaction):
        if interaction.user not in self.players or len(self.players) < 7:
            self.players.append(interaction.user)
            await interaction.response.send_message("You have joined the game of Black Jack!", ephemeral=True)
            await interaction.message.edit(embed=self.create_embed())
        elif len(self.players) >= 7:
            await interaction.response.send_message("The game is full!", ephemeral=True)
        else:
            await interaction.response.send_message("You are already in this game!", ephemeral=True)
    