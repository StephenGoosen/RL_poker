from game.cards import Card

class Player:
    ''' 
    Representation of a player

    Contains:
        The name of the player.
        The position of the player.
        The list of cards in their hand
    '''
    def __init__(self, name: str):
        self.name = name
        self.hand = []

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