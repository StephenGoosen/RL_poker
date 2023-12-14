class Table:

    def __init__(self):
        self.flop = []
        self.turncard = None
        self.rivercard = None

    def reveal_flop(self, flop_cards):
        if len(self.flop) == 0:
            self.flop = flop_cards

            flop_card1 = flop_cards[0]
            flop_card2 = flop_cards[1]
            flop_card3 = flop_cards[2]

            print(f"Flop: {flop_card1}, {flop_card2}, {flop_card3}")
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