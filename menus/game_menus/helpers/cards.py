import random


class Card:
    def __init__(self):
        self.number = None
        self.suit = None
        self.color = None
    
    def __repr__(self) -> str:
        return f"Number: {self.number}, Suite: {self.suit}, Color: {self.color}"
    
    def add_number(self, number):
        self.number = number
        return self
    
    def add_suit(self, suit):
        self.suit = suit
        return self
    
    def add_color(self, color):
        self.color = color
        return self
    

suites = ["spades", "hearts", "diamonds", "clubs"]
colors = ["red", "black"]


def random_card() -> Card:
    return Card().add_number(random.randint(1, 13)).add_suit(''.join(random.choice(suites))).add_color(''.join(random.choice(colors)))


def deal_deck(amount):
    deck = {"cards": []}
    
    for n in range(amount):
        deck["cards"].append(random_card())
    
    return deck


def deal_cards(amount_per, deck_amount):
    decks = []
    
    for i in range(deck_amount):
        deck = deal_deck(amount_per)
        decks.append(deck)
    
    return decks


def add_card(deck, card: Card):
    print(card)
    deck["cards"].append(card)
