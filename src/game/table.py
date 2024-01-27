# table.py

import game.config as cg
import numpy as np

class Community_Cards:
    def __init__(self):
        self.flopcards = []
        self.turncard = None
        self.rivercard = None

    def reset(self):
        self.flopcards = []
        self.turncard = None
        self.rivercard = None 

    def insert_flop(self, flopcards):
        if not self.flopcards:
            self.flopcards = flopcards
        else:
            print("Flop has already been inserted.")

    def insert_turn(self, turncard):
        if self.turncard is None:
            self.turncard = turncard
        else:
            print("Turn card has already been inserted.")

    def insert_river(self, rivercard):
        if self.rivercard is None:
            self.rivercard = rivercard
        else:
            print("River card has already been inserted.")

    def reveal_flop(self):
            print(f"Flop: {', '.join(map(str, self.flopcards))}")
            return self.flopcards


    def reveal_turn(self):
        if self.turncard is not None:
            print("Turn:", str(self.turncard))
            return self.turncard
        else:
            print("Turn card has already been revealed.")


    def reveal_river(self):
        if self.rivercard is not None:
            print("River:", str(self.rivercard))
            return self.rivercard
        else:
            print("River card has already been revealed.")
