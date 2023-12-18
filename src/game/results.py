# results.py

class Results:
    '''
    Stores the players' names, hands, and bets.
    Stores the community cards.
    Stores decisions.
    Stores Hand Winner.
    Can be used for analysis of performance.

    '''

    def __init__(self):
        self.players = []
        self.community_cards = []
        self.decisions = []
        self.hand_winner = None

    def add_player(self, player):
        self.players.append(player)

    def add_community_cards(self, cards):
        self.community_cards.extend(cards)

    def add_decision(self, decision):
        self.decisions.append(decision)

    def set_hand_winner(self, player):
        self.hand_winner = player

    def get_players(self):
        return self.players

    def get_community_cards(self):
        return self.community_cards

    def get_decisions(self):
        return self.decisions

    def get_hand_winner(self):
        return self.hand_winner

    def get_results(self):
        return {
            'players': self.players,
            'community_cards': self.community_cards,
            'decisions': self.decisions,
            'hand_winner': self.hand_winner
        }