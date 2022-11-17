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


class Cell(dict):
    def __init__(self, color, taken):
        self['color'] = color
        self['taken'] = taken
    
    def __repr__(self) -> str:
        return self['color']


class Row:
    def __init__(self, *items):
        self.items = []
        for item in items:
            self.items.append(item)

    def __getitem__(self, key):
        return self.items[key]
    
    def __setitem__(self, key, value):
        self.items[key] = value
    
    def __repr__(self) -> str:
        s = ""
        for cell in self.items:
            s += str(cell)
        
        return s
    
    def __len__(self):
        return len(self.items)
    
    def append(self, item):
        self.items.append(item)


class Board:
    def __init__(self, x, y):
        self.width = x
        self.height = y
        self.rows = []
        self.winner = False
        for r in range(x):
            row = Row()
            for c in range(y):
                row.append(Cell(color='⬛', taken=False))
            self.rows.append(row)
    
    def __getitem__(self, key):
        return self.rows[key]
    
    def __repr__(self) -> str:
        s = ""

        zipped = list(zip(*self.rows))
        for i in range(len(zipped) - 1, -1, - 1):
            for element in zipped[i]:
                s += str(element)
            s += '\n'

        return s
    
    def get_lowest_point(self, row):
        for i, cell in enumerate(row):
            if not cell['taken']:
                return i
        return self.height

    def change_cell(self, row, index, color):
        if index != self.height:
            row[index]['color'] = color
            row[index]['taken'] = True
        else:
            print("This column is full!")
        if self.__check_for_match():
            self.winner = True

    def __check_for_match(self):
        if self.__check_for_vertical() or self.__check_for_horizontal() or self.__check_for_diagonal():
            return True

    def __check_for_vertical(self):
        for row in self.rows:
            diff = 1
            for i, cell in enumerate(row):
                if not i + 1 >= len(row) - 1:
                    next = row[i + 1]

                    if next['taken'] and next['color'] == cell['color']:
                        diff += 1
                if diff >= 4:
                    return True
        
        return False
    
    def __check_for_horizontal(self):
        zipped = list(zip(*self.rows))

        for row in zipped:
            diff = 1
            for i, cell in enumerate(row):
                if not i + 1 >= len(row) - 1:
                    next = row[i + 1]

                    if next['taken'] and next['color'] == cell['color']:
                        diff += 1
                if diff >= 4:
                    return True
        
        return False

    def __check_for_diagonal(self):
        for r, row in enumerate(self.rows):
            for i, cell in enumerate(row):
                diff = 1
                current_x = i
                current_y = r
                current_cell = cell

                while True:
                    if current_x + 1 >= len(row) or current_y + 1 >= len(self.rows):
                        if diff >= 4:
                            return True
                        break
                    else:
                        next_cell = self.rows[current_y + 1][current_x + 1]

                        if not next_cell["taken"]:
                            if diff >= 4:
                                return True
                            break
                        elif next_cell["color"] == current_cell["color"]:
                            diff += 1
                            if diff >= 4:
                                return True
                    current_x += 1
                    current_y += 1
                    current_cell = next_cell

                diff = 1
                current_x = i
                current_y = r
                current_cell = cell

                while True:
                    if current_x - 1 >= len(row) or current_y + 1 >= len(self.rows):
                        if diff >= 4:
                            return True
                        break
                    else:
                        next_cell = self.rows[current_y + 1][current_x - 1]

                        if not next_cell["taken"]:
                            if diff >= 4:
                                return True
                            break
                        elif next_cell["color"] == current_cell["color"]:
                            diff += 1
                            if diff >= 4:
                                return True
                    current_x -= 1
                    current_y += 1
                    current_cell = next_cell      

        return False


class ConnectFourGame(discord.ui.View):
    def __init__(self, red_player, yellow_player):
        super().__init__()
        self.red_player = red_player
        self.yellow_player = yellow_player
        self.other_player = yellow_player
        self.current_player = red_player
        self.row_buttons = []
        self.winner = None
        self.board = Board(7, 6)

        
        for row in range(1, 8):
            self.row_buttons.append(discord.ui.Button(
                label=row, style=discord.ButtonStyle.gray, 
                custom_id=''.join(random.choices(string.ascii_letters + string.digits, k=20))))
        
        for button in self.row_buttons:
            button.callback = self.button_callback_event
            self.add_item(button)
    
    def create_embed(self):
        embed = discord.Embed(title="Connect Four", description=str(self.board))
        if self.winner != None:
            embed.add_field(name="Winner!", value=f"{self.winner['plr']} {self.winner['color']} has won the game of Connect Four!")
        return embed

    async def button_callback_event(self, interaction: discord.Interaction):
        current = self.__find_index_from_id(interaction.data["custom_id"])
        
        if self.winner == None:
            if interaction.user == self.current_player["plr"]:
                row = self.board[current]
                
                c = self.board.get_lowest_point(row=row)
                if c == 6:
                    await interaction.response.send_message("This column is full!", ephemeral=True)
                else:
                    self.board.change_cell(row=row, index=c, color=self.current_player["color"])
                    if self.board.winner:
                        self.winner = self.current_player
                        await interaction.message.edit(embed=self.create_embed())

                    self.current_player, self.other_player = self.other_player, self.current_player
                    await interaction.message.edit(embed=self.create_embed())
            elif interaction.user == self.other_player["plr"]:
                await interaction.response.send_message("It is not your turn yet!", ephemeral=True)
            else:
                await interaction.response.send_message("You are not a part of this game!", ephemeral=True)
                
            
            await interaction.response.send_message(current + 1, ephemeral=True)
        else:
            await interaction.response.send_message(f"{self.winner['plr']} already won!", ephemeral=True)

    def __find_index_from_id(self, id):
        for i, button in enumerate(self.row_buttons):
            if button.custom_id == id:
                return i
        return 0
    