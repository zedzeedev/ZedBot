class Cell(dict):
    def __init__(self, color, taken):
        self['color'] = color
        self['taken'] = taken
    
    def __repr__(self) -> str:
        return self['color']
    

class Board:
    def __init__(self, x, y, num_to_match):
        self.height = y
        self.width = x
        self.board = {}
        self.winner = False
        self.num_to_match = num_to_match
        
        for col in range(y + 1):
            for row in range(x + 1):
                self.board[row, col] = Cell("⬛", False)
    
    def __getitem__(self, key) -> Cell:
        return self.board[key]   
    
    def __setitem__(self, key, value):
        self.board[key] = value
        if self.find_match():
            self.winner = True
    
    def __repr__(self) -> str:
        s = ""
        
        for col in range(self.height):
            for row in range(self.width):
                current_str = str(self[row, col])
                if row == self.width - 1:
                    current_str += '\n'
                s += current_str
        return s

    def reverse_str(self) -> str:
        s = ""
        
        for col in range(self.height - 1, -1, -1):
            for row in range(self.width):
                current_str = str(self[row, col])
                if row == self.width - 1:
                    current_str += '\n'
                s += current_str
        return s
    
    def find_match(self):
        if self.__find_vertical() or self.__find_horizontal() or self.__find_diagonal():
            self.winner = True
                        
        return False 
    
    def find_lowest_point(self, row):
        for col in range(self.height):
            if not self[row, col]['taken']:
                return col
        return self.height
                    
    
    def __find_vertical(self):
        for col in range(self.height):
            for row in range(self.width):
                current_cell = self.board[row, col]
                current = col
                diff = 1
                
                for i in range(self.num_to_match):
                    if current + 1 <= self.height:
                        next_cell = self.board[row, current + 1]
                        
                        if next_cell['taken'] and next_cell['color'] == current_cell['color']:
                            diff += 1
                            if diff >= self.num_to_match:
                                return True
                    current_cell = next_cell
                    current += 1
                    if diff >= self.num_to_match:
                        return True
                        
        return False     

    def __find_horizontal(self):
        for col in range(self.height):
            for row in range(self.width):
                current_cell = self.board[row, col]
                current = row
                diff = 1
                
                for i in range(self.num_to_match):
                    if current + 1 <= self.width:
                        next_cell = self.board[current + 1, col]
                        
                        if next_cell['taken'] and next_cell['color'] == current_cell['color']:
                            diff += 1
                            if diff >= self.num_to_match:
                                return True
                    current_cell = next_cell
                    current += 1
                    if diff >= self.num_to_match:
                        return True
                        
        return False     
    
    def __find_diagonal(self):
        for col in range(self.height):
            for row in range(self.width):
                current_cell = self.board[row, col]
                current_x = row
                current_y = col
                diff = 1
                
                for i in range(self.num_to_match):
                    if current_x + 1 <= self.width and current_y + 1 <= self.height:
                        next_cell = self.board[current_x + 1, current_y + 1]
                        
                        if next_cell['taken'] and next_cell['color'] == current_cell['color']:
                            diff += 1
                            if diff >= self.num_to_match:
                                return True
                    current_cell = next_cell
                    current_x += 1
                    current_y += 1
                    if diff >= self.num_to_match:
                        return True
                current_cell = self.board[row, col]
                current_x = row
                current_y = col
                diff = 1
                
                for i in range(self.num_to_match):
                    if current_x - 1 >= self.width and current_y + 1 <= self.height:
                        next_cell = self.board[current_x - 1, current_y + 1]
                        
                        if next_cell['taken'] and next_cell['color'] == current_cell['color']:
                            diff += 1
                            if diff >= self.num_to_match:
                                return True
                    current_cell = next_cell
                    current_x -= 1
                    current_y += 1
                    if diff >= self.num_to_match:
                        return True
                        
        return False     
