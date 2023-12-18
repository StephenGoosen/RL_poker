# table.py

import os

from game.player import Player

class Current_Players:
    def __init__(self, player_list):
        self.players = [Player(name) for name in player_list]

class Community_Cards:
    def __init__(self):
        self.flop = []
        self.turncard = None
        self.rivercard = None

    def reveal_flop(self, flop_cards):
        if not self.flop:
            self.flop = flop_cards
            print(f"Flop: {', '.join(map(str, flop_cards))}")
        else:
            print("Flop has already been revealed.")

    def reveal_turn(self, turn_card):
        if self.turncard is None:
            self.turncard = turn_card
            print("Turn:", str(self.turncard))
        else:
            print("Turn card has already been revealed.")

    def reveal_river(self, river_card):
        if self.rivercard is None:
            self.rivercard = river_card
            print("River:", str(self.rivercard))
        else:
            print("River card has already been revealed.")

class Player_Cards:
    def __init__(self, player_list, deck):
        self.current_players = Current_Players(player_list)
        self.deck = deck
        self.hands = {player.name: [] for player in self.current_players.players}

    def deal_cards(self):
        for _ in range(2):
            for player in self.current_players.players:
                card = self.deck.deal_card()
                player.receive_card(card)
                self.hands[player.name].append(card)
