# cards.py

import os
import random

from pokereval.card import Card  # Import the Card class from the pokereval library

class Deck:
    ''' 
    Representation of a Standard Deck

    Contains a list of the cards in the deck

    '''

    def __init__(self):
        self.cards = []

        suits = Card(2,1).SUIT_TO_STRING
        ranks = Card(2,1).RANK_TO_STRING

        for suit in suits:
            for rank in ranks:
                _card = Card(rank, suit)
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