import random

card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
card_suits = ["Spades", "Hearts", "Diamonds", "Clubs"]

class Card:
    '''
    Representation of a Playing Card

    Contains a value: from 2 to 14. Standard number values and face cards from 11 to 14 (Ace)

    Contains a suit: spades, clubs, hearts, and diamonds.
    '''

    def __init__(self, value, suit):
        if isinstance(value, str):
            face_cards = {
                "J": 11,
                "Q": 12,
                "K": 13,
                "A": 14
            }
            self.value = face_cards.get(value.upper(), int(value))
        else:
            self.value = int(value)
        self.suit = suit

    def __str__(self):
        ''' 
        String output for display purposes
        '''
        face_cards = {
            11: "J",
            12: "Q",
            13: "K",
            14: "A"
        }

        display_value = face_cards.get(self.value, str(self.value))
        return f"{display_value} of {self.suit}"

class Deck:
    ''' 
    Representation of a Standard Deck

    Contains a list of the cards in the deck
    '''

    def __init__(self):
        self.cards = []
        values = card_values
        suits = card_suits

        for suit in suits:
            for value in values:
                _card = Card(value, suit)
                self.cards.append(_card)

    def shuffle(self):
        ''' 
        Shuffles the deck
        '''
        random.shuffle(self.cards)

    def deal_card(self):
        ''' 
        Deals a single card from the deck
        '''
        return self.cards.pop()