# players.py

from pokereval.card import Card

import game.game_logic as gl
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
        self.hole_cards = []
        self.hand = []
        self.hand_strength = 0.0
        self.hand_description = ""
        self.chipcount = cg.chipcount

        self.bet = 0
        self.folded = False
        self.all_in = False
        self.round_played = False

        self.game_in_play = True

    def reset_betting(self):
        self.bet = 0
        self.round_played = False

    def reset_round(self):
        self.reset_betting()
        self.reset_hand()
        self.folded = False
        self.all_in = False
        self.round_played = False

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
        self.hand_strength = 0.0
        self.hand_description = ""

    def set_hand_info(self, hand_strength, hand_description):
        '''
        Sets the hand strength and description
        '''
        self.hand_strength = hand_strength
        self.hand_description = hand_description

    def __str__ (self):
        return f"{self.name}"
