class Card(dict):
    def __init__(self, suite, number, color):
        self.suite = suite
        self.number = number
        self.color = color
    
    def __getitem__(self, key):
        return self[key]
    
    def __setitem__(self, key, value):
        self[key] = value
