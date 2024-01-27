# cards.py

import os
import random
import re

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
    
def change_card_str(card):
    '''
    Converts Card object string representation for better display.
    '''

    rank_mapping = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    suit_mapping = {'s': 'spades', 'h': 'hearts', 'd': 'diamonds', 'c': 'clubs'}

    rank_match = re.findall(r'\((.*?)\)', str(card))[0][0]
    suit_match = re.findall(r'\((.*?)\)', str(card))[0][1]

    rank = rank_mapping.get(rank_match, rank_match)
    suit = suit_mapping.get(suit_match, suit_match)

    return rank, suit

def change_card_num(card):
    '''
    Converts Card object numerical representation for machine learning.
    '''
    rank_mapping = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    suit_mapping = {'s': 1, 'h': 2, 'd': 3, 'c': 4}

    rank_match = re.findall(r'\((.*?)\)', str(card))[0][0]
    suit_match = re.findall(r'\((.*?)\)', str(card))[0][1]

    rank = rank_mapping.get(rank_match, rank_match)
    suit = suit_mapping.get(suit_match, suit_match)

    return [rank, suit]
