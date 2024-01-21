# players.py

from pokereval.card import Card

import game.config as cg

class Player:
    ''' 
    Representation of a player

    Contains:
        The name of the player.
        The list of cards in their hand
    '''

    def __init__(self, name: str):
        self.name = name
        self.hand = []
        self.hand_strength = 0.0
        self.hand_description = ""
        self.chipcount = cg.chipcount
        self.in_play = True

    def in_play(self, in_play: bool):
        if in_play == True:
            self.in_play = True
        else:
            self.in_play = False

    def receive_card(self, card: Card):
        ''' 
        Receives a single card appended to the hand list
        '''

        self.hand.append(card)

    def show_hand(self):
        ''' 
        Prints hand out
        '''

        print(f"{self.name}'s hand:")
        for card in self.hand:
            print(card)

    def reset_hand(self):
        ''' 
        Resets the hand list
        '''

        self.hand = []

    def set_hand_info(self, strength, description):
        '''
        Contains hand strength score and description
        '''
        self.hand_strength = strength
        self.hand_description = description

    def chip_count(self):
        '''
        Returns the number of chips the player has
        '''
        return self.chipcount

    def add_chip(self, chip):
        self.chipcount += chip

    def remove_chip(self, chip):
        self.chipcount -= chip

    def __str__ (self):
        return f"{self.name}"
