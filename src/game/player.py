# players.py

from pokereval.card import Card

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
        self.hand_strength = float(strength)
        self.hand_description = description