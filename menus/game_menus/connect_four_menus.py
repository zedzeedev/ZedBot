import discord
import random
import string


class StartMenu(discord.ui.View):
    def __init__(self, player1: discord.User, player2: discord.User):
        super().__init__()
        self.red_player = player1
        self.yellow_player = player2
        self.match_accepted = False
    
    def create_embed(self):
        embed = discord.Embed(title="Connect Four", description=f"{self.red_player['plr']} would like to play Connect Four with {self.yellow_player['plr']}")

        return embed
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept_button_callback(self, button, interaction: discord.Interaction):
        if self.__is_second_player(interaction.user) and not self.match_accepted:
            self.match_accepted = True
            game_menu = ConnectFourGame(self.red_player, self.yellow_player)
            await interaction.response.send_message(embed=game_menu.create_embed(), view=game_menu)
        elif self.match_accepted:
            await interaction.response.send_message(f"This match has already started!")
        else:
            await interaction.response.send_message(f"You are not the requested user!", ephemeral=True)
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline_button_callback(self, button, interaction: discord.Interaction):
        if self.__is_second_player(interaction.user):
            self.match_accepted = False
            await interaction.response.send_message(f"{self.yellow_player['plr']} has declined your Connect Four request!")
        else:
            await interaction.response.send_message(f"You are not the requested user!")
            
    def __is_second_player(self, plr: discord.User):
        return plr == self.yellow_player["plr"]


class ConnectFourGame(discord.ui.View):
    def __init__(self, red_player, yellow_player):
        super().__init__()
        self.red_player = red_player
        self.yellow_player = yellow_player
        self.other_player = yellow_player
        self.current_player = red_player
        self.rows = []
        self.row_buttons = []
        self.winner = None

        for r in range(1, 8):
            row = []
            for col in range(1, 7):
                row.append({"color": "⬛", "height": col, "taken": False})
            self.rows.append(row)
        
        for row in range(1, len(self.rows) + 1):
            self.row_buttons.append(discord.ui.Button(
                label=row, style=discord.ButtonStyle.gray, 
                custom_id=''.join(random.choices(string.ascii_letters + string.digits, k=20))))
        
        for button in self.row_buttons:
            button.callback = self.button_callback_event
            self.add_item(button)
    
    def create_embed(self):
        s = ""
        for c in range(5, -1, -1):
            for r, row in enumerate(self.rows):
                col = row[c]

                s += col["color"]
                if r == len(self.rows) - 1:
                    s += "\n"
        
        embed = discord.Embed(title="Connect Four", description=s)
        if self.winner != None:
            embed.add_field(name="Winner!", value=f"{self.winner['plr']} has won the game of Connect Four!")
        return embed

    async def button_callback_event(self, interaction: discord.Interaction):
        current = self.__find_index_from_id(interaction.data["custom_id"])
        
        if self.winner == None:
            if interaction.user == self.current_player["plr"]:
                row = self.rows[current]
                
                c = self.__find_lowest_point(row=row)
                if c == 6:
                    await interaction.response.send_message("This column is full!", ephemeral=True)
                else:
                    col = row[c]
                    col["color"] = self.current_player["color"]
                    col["taken"] = True
                    if self.__find_match():
                        await interaction.message.edit(embed=self.create_embed())

                    self.current_player, self.other_player = self.other_player, self.current_player
                    await interaction.message.edit(embed=self.create_embed())
            elif interaction.user == self.other_player["plr"]:
                await interaction.response.send_message("It is not your turn yet!", ephemeral=True)
            else:
                await interaction.response.send_message("You are not a part of this game!", ephemeral=True)
                
            
            await interaction.response.send_message(current, ephemeral=True)
        else:
            await interaction.response.send_message(f"{self.winner['plr']} already won!", ephemeral=True)

    def __find_index_from_id(self, id):
        for i, button in enumerate(self.row_buttons):
            if button.custom_id == id:
                return i
        return 0
    
    def __find_lowest_point(self, row):
        for i, col in enumerate(row):
            if not col["taken"]:
                return i
        return 6
    
    def __find_match(self):
        for row in self.rows:
            if self.__find_vertical_match(row=row):
                self.winner = self.current_player
                print("vertical match")
                return True
        if self.__find_horizontal_match():
            self.winner = self.current_player
            print("horizontal match")
            return True
        if self.__find_diagonal_match():
            self.winner = self.current_player
            print("diagonal match")
            return True
        return False
    
    def __find_vertical_match(self, row):
        diff = 1

        for i, col in enumerate(row):
            if i + 1 >= len(row) - 1:
                if diff >= 4:
                    return True
                diff = 1
            else:
                next = row[i + 1]

                if not next["taken"]:
                    if diff >= 4:
                        return True
                    diff = 1

                if next["color"] == col["color"]:
                    diff += 1
                    if diff >= 4:
                        return True
        else:
            if diff >= 4:
                return True
            diff = 1
    
        return False

    def __find_horizontal_match(self):
        diff = 1
        heights = self.__split_into_heights()

        for row in heights:
            for i, height in enumerate(row):
                if i + 1 >= len(row) - 1:
                    if diff >= 4:
                        return True
                    diff = 1
                else:
                    next = row[i + 1]

                    if not next["taken"]:
                        if diff >= 4:
                            return True
                        diff = 1
                    elif next["color"] == height["color"]:
                        diff += 1
                        if diff >= 4:
                            return True
            else:
                if diff >= 4:
                    return True
                diff = 1

        return False
    
    def __find_diagonal_match(self):
        diff = 1
        heights = self.__split_into_heights()
        
        for r, row in enumerate(heights):
            for i, height in enumerate(row):
                if i + 1 >= len(row) - 1 or r + 1 >= len(heights) - 1:
                    if diff >= 4:
                        return True
                    diff = 1
                else:
                    next = heights[r + 1][i + 1]
                    
                    if not next["taken"]:
                        if diff >= 4:
                            return True
                        diff = 1
                    elif next["color"] == height["color"]:
                        diff += 1
                        if diff >= 4:
                            return True
        else:
            if diff >= 4:
                return True
            diff = 1
            
        return False 

    def __split_into_heights(self):
        heights = []

        for row in self.rows:
            for col in row:
                h = col["height"]

                if h >= len(heights):
                    heights.append([col])
                else:
                    heights[h - 1].append(col)
        
        return heights