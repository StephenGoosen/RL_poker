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


'''
Temporarily replacing Chipset with a simple single integer value representing chip count

class Chipset:
    def __init__(self):
        self.chips = np.zeros(5, dtype=int)
        self.starter_chipset = cg.starter_chipset
        self.total_value = 0

    def reset_chipset(self):
        self.chips = np.zeros(5, dtype=int)

    def reset_starter_chipset(self):
        self.chips = self.starter_chipset.values

    def add_chips(self, chips):
        self.chips += chips

    def remove_chips(self, chips):
        self.chips -= chips

    def bet_to_chips(bet: int):
        chip_values = cg.chip_values

        number_of_chips = {
            "white": 0,
            "red": 0,
            "green": 0,
            "blue": 0,
            "black": 0
        }

        for chip_color in ["black", "blue", "green", "red", "white"]:
            chip_value = chip_values[chip_color]
            
            chips_needed = bet // chip_value
            number_of_chips[chip_color] = chips_needed
            bet -= chip_value * chips_needed

        return number_of_chips
    
    def chip_colour_to_value(self, colour):
        return cg.chip_values[colour]

    def calculate_total_value(self):
        for index, value in enumerate(self.chips):
            x = value * cg.chip_values[list(cg.chip_values.keys())[index]]
            self.total_value += x
        return self.total_value

class Pot:
    def __init__(self):
        self.chips = Chipset().chips

    def add_chip(self, chip):
        self.chips.append(chip)

    def give_chips(self, players):
        num_players = len(players)
        
        if num_players == 0:
            print(f"Error no winners.")
        
        split_amount = [chip // num_players for chip in self.chips]
        
        for i in range(num_players):
            player = players[i]
            for j in range(5):
                player.add_chip(split_amount[j])

        self.chips.reset_chipset()

'''
