# game_logic.py

import random  as rd
import numpy as np
import itertools

from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator

from game.cards import change_card_str, Deck
import game.config as cg
import game.player as gp
import game.table as tb

agents = cg.agents

#Chipset Temporarily Removed
'''

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

def remove_chips_from_player(player_chips, chips_to_remove):
    for chip_color, count in chips_to_remove.items():
        player_chips[chip_color] -= count
        player_chips[chip_color] = max(0, player_chips[chip_color])
'''

class Hand:
    def __init__(self, hole_cards, community_cards):
        self.cards = hole_cards + community_cards
        self.ranks = []
        self.suits = []

        for card in self.cards:
            rank, suit = change_card_str(card)
            self.ranks.append(rank)
            self.suits.append(suit)

    def royal_flush(self):
        royal_ranks = set([10, 11, 12, 13, 14])

        cards_by_suit = {}
        for card in self.cards:
            cards_by_suit.setdefault(card.suit, []).append(card)

        for suit, cards in cards_by_suit.items():
            royal_cards = [card for card in cards if card.rank in royal_ranks]

            if len(royal_cards) == 5:
                ordered = sorted(royal_cards, key=lambda card: card.rank)
                return {"hand_type": "Royal Flush!", "cards": [card.rank for card in ordered]}

        return None
    
    def straight_flush(self):
        cards_by_suit = {}
        for card in self.cards:
            cards_by_suit.setdefault(card.suit, []).append(card)

        for suit, cards in cards_by_suit.items():
            if len(cards) >= 5:
                ordered = sorted(cards, key=lambda card: card.rank)

                for i in range(len(ordered) - 4):
                    if all(ordered[i + j].rank == (ordered[i].rank + j) % 14 + 1 for j in range(5)):
                        return {"hand_type": "Straight Flush", "cards": [card.rank for card in ordered[i:i + 5]]}

                if {14, 2, 3, 4, 5}.issubset(card.rank for card in ordered):
                    return {"hand_type": "Straight Flush", "cards": [1, 2, 3, 4, 5]}

        return None

    def four_of_a_kind(self):
        for rank in set(card.rank for card in self.cards):
            rank_cards = [card for card in self.cards if card.rank == rank]
            if len(rank_cards) == 4:
                other_card = next(card for card in self.cards if card.rank != rank)
                return {"hand_type": "Four of a Kind", "cards": [card.rank for card in rank_cards] + [other_card.rank]}

        return None

    def full_house(self):
        for rank in set(card.rank for card in self.cards):
            rank_cards = [card for card in self.cards if card.rank == rank]

            if len(rank_cards) == 3:
                other_rank = next(other_rank for other_rank in set(card.rank for card in self.cards) if other_rank != rank)
                other_rank_cards = [card for card in self.cards if card.rank == other_rank]
                if len(other_rank_cards) >= 2:
                    return {"hand_type": "Full House", "cards": [card.rank for card in rank_cards + other_rank_cards[:2]]}
        
        return None
    
    def flush(self):
        for suit in set(card.suit for card in self.cards):
            suit_cards = [card for card in self.cards if card.suit == suit]
            if len(suit_cards) >= 5:
                ordered = sorted(suit_cards, key=lambda card: card.rank, reverse=True)
                return {"hand_type": "Flush", "cards": [card.rank for card in ordered[:5]]}

        return None

    def straight(self):
        unique_ranks = set(card.rank for card in self.cards)
        if len(unique_ranks) < 5:
            return None

        sorted_ranks = sorted(unique_ranks)
        for i in range(len(sorted_ranks) - 4):
            if all(sorted_ranks[i + j] == sorted_ranks[i] + j for j in range(5)):
                return {"hand_type": "Straight", "cards": [r for r in range(sorted_ranks[i], sorted_ranks[i] + 5)]}

        if 14 in unique_ranks and 2 in unique_ranks and 3 in unique_ranks and 4 in unique_ranks and 5 in unique_ranks:
            return {"hand_type": "Straight", "cards": [14, 2, 3, 4, 5]}

        return None

    def three_of_a_kind(self):
        for rank in set(card.rank for card in self.cards):
            rank_cards = [card for card in self.cards if card.rank == rank]
            if len(rank_cards) == 3:
                other_cards = [card for card in self.cards if card.rank != rank]
                return {"hand_type": "Three of a Kind", "cards": [card.rank for card in rank_cards] + [other_cards[0].rank, other_cards[1].rank]}

        return None

    def two_pair(self):
        rank_counts = {}
        for card in self.cards:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1

        pairs = [rank for rank, count in rank_counts.items() if count == 2]

        if len(pairs) >= 2:
            ordered_pairs = sorted(pairs, reverse=True)
            kicker = next(card.rank for card in self.cards if card.rank not in ordered_pairs)

            return {"hand_type": "Two Pair", "cards": ordered_pairs + [kicker]}

        return None

    def one_pair(self):
        pairs = [rank for rank in set(self.ranks) if self.ranks.count(rank) == 2]

        if len(pairs) == 1:
            unique_ranks = sorted(set(self.ranks) - set(pairs), reverse=True)
            
            return {"hand_type": "One Pair", "cards": pairs + unique_ranks[:3]}

        return None

    def high_card(self):
        ordered_cards = sorted(self.cards, key=lambda card: card.rank, reverse=True)
        return {"hand_type": "High Card", "cards": [ordered_cards[0].rank]}


    def determine_hand(self):
        hand_checks = [
            (self.royal_flush, "Royal Flush"),
            (self.straight_flush, "Straight Flush"),
            (self.four_of_a_kind, "Four of a Kind"),
            (self.full_house, "Full House"),
            (self.flush, "Flush"),
            (self.straight, "Straight"),
            (self.three_of_a_kind, "Three of a Kind"),
            (self.two_pair, "Two Pair"),
            (self.one_pair, "One Pair"),
            (self.high_card, "High Card"),
        ]

        for check_function, hand_type in hand_checks:
            result = check_function()
            if result:
                result["hand_type"] = hand_type
                return result

        return None

def compare_scores(score_dict):
    # Hand dict has the player name and the players score

    # Loop through each
    player_scores = {}
    for name, score in score_dict.items():
        player_scores[name] = score

    # Sort by score and return highest score/scores
    sorted_scores = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[0][0]

def hand_evaluation(player, hole_cards, community_cards):
    # Use HandEvaluator to get the hand score
    score = HandEvaluator.evaluate_hand(hole_cards, community_cards)

    # Use Hand to get the hand description
    hand_results = Hand(hole_cards, community_cards).determine_hand()

    # Set hand information for the player
    player.set_hand_info(score, hand_results['hand_type'])

    # Return the score and hand results
    return score, hand_results

class GameLogic:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.pot = 0
        self.pre_flop_pot = np.zeros(len(cg.agents))
        self.pre_turn_pot = np.zeros(len(cg.agents))
        self.pre_river_pot = np.zeros(len(cg.agents))
        self.showdown_pot = np.zeros(len(cg.agents))

        self.small_blind = cg.small_blind
        self.big_blind = cg.big_blind

        self.players = []
        for agent in agents:
            player = gp.Player(agent)
            self.players.append(player)
        rd.shuffle(self.players)

        self.dealer_index = 0
        self.small_blind_index = (self.dealer_index + 1) % len(self.players)
        self.big_blind_index = (self.small_blind_index + 1) % len(self.players)
        self.active_player_index = (self.big_blind_index + 1) % len(self.players)

        self.community_cards = tb.Community_Cards()

        for player in self.players:
            print(f"{player.name} has {player.chipcount} chips")

        self.players_dealt = False
        self.flop_dealt = False
        self.turn_dealt = False
        self.river_dealt = False
        self.game_over = False

    def rotate_positions(self):
        # Rotate dealer index
        self.dealer_index = (self.dealer_index + 1) % len(self.players)

        # Rotate small blind index
        self.small_blind_index = (self.small_blind_index + 1) % len(self.players)

        # Rotate big blind index
        self.big_blind_index = (self.big_blind_index + 1) % len(self.players)

        # Rotate active player index
        self.active_player_index = (self.active_player_index + 1) % len(self.players)

    def get_active_player(self):
        return self.players[self.active_player_index]
    
    def get_dealer(self):
        return self.players[self.dealer_index]

    def get_small_blind(self):
        return self.players[self.small_blind_index]

    def get_big_blind(self):
        return self.players[self.big_blind_index]

    def initialize_gamestate(self):
        '''        
        Determine who is small blind and big blind
        Set dealer
        Rotate
        Set active player
        '''

        # Determine small and big blind index
        dealer_index = 0
        small_blind_index = (dealer_index + 1) % len(self.players)
        big_blind_index = (small_blind_index) + 1 % len(self.players)

        # Remove blind values from players.chipset
        #self.players[small_blind_index].chipset.remove_chip('white')
        #self.players[big_blind_index].chipset.remove_chip('red')

        # Set active player
        active_player_index = (dealer_index + 1) % len(self.players)
        #self.players[active_player_index].set_active()

    def new_round(self):
        # Resets the game state for a new round
        # Resets Deck
        # Shuffles Deck
        # Rotates small and big blind and dealer
        # Sets active player
        self.deck = Deck()
        self.deck.shuffle()
        self.pot = 0
        self.rotate_positions()
        self.players_in_play = np.ones(len(self.players))
        self.active_player_index = (self.dealer_index + 1) % len(self.players)

    def deal_hole_cards(self):
        for player in self.players:
            player.hand.append(self.deck.deal_card())

        for player in self.players:
            player.hand.append(self.deck.deal_card())
    
    def betting_round(self):
        # Start from active player in players_in_play vector
        self.current_bet = 0
        active_player = self.active_player_index
        print(self.active_player_index)
        num_players = len(self.players)
        print(f"Number of players: {num_players}")

        for _ in range(num_players):
            if active_player < num_players:
                current_player = self.players[active_player]
                bet_amount = self.request_bet(current_player)
                current_player.chipcount -= bet_amount
                self.current_bet += bet_amount
                active_player = (active_player + 1) % num_players
                print(f"Current bet: {self.current_bet}, Active player: {active_player}")
            else:
                print("Warning: active_player index exceeds the number of players.")
                break

        self.pot += self.current_bet


    def check(self, player):
        pass

    def call(self, player):
        bet_amount = self.current_bet - player.chipcount
        player.remove_chip(bet_amount)
        self.pot += bet_amount

    def request_bet(self, player):
        try:
            bet_amount = int(input(f"{player.name}, enter your bet amount: "))
        except ValueError:
            print("Invalid input. Please enter a valid bet amount.")
            return self.request_bet(player)

        # Validate the bet amount
        if bet_amount < 0 or bet_amount > player.chipcount:
            print("Invalid bet amount. Please enter a valid amount within your chip range.")
            return self.request_bet(player)

        return bet_amount

    def get_active_player(self):
        # Return the current active player
        for player in self.players:
            if player.is_active():
                return player
            
    def pre_flop(self):
        self.betting_round()

    def flop(self):
        self.deck.deal_card()  # burn card
        self.flop_cards = [self.deck.deal_card() for _ in range(3)]
        self.community_cards.insert_flop(self.flop_cards)
        return self.flop_dealt == True

    def pre_turn(self):
        #pre-turn betting
        pass

    def turn(self):
        self.deck.deal_card()  # burn card
        self.turn_card = self.deck.deal_card()
        self.community_cards.insert_turn(self.turn_card)
        return self.turn_dealt == True


    def pre_river(self):
        #pre-river betting
        pass

    def river(self):
        self.deck.deal_card()  # burn card
        self.river_card = self.deck.deal_card()
        self.community_cards.insert_river(self.river_card)
        return self.river_dealt == True

    def showdown():
        pass

    def end_round(self):
        self.community_cards.reset()
        self.pot = 0
        self.current_bet = 0
        self.players_dealt = False
        self.flop_dealt = False
        self.turn_dealt = False
        self.river_dealt = False
        self.deck = Deck()
        self.deck.shuffle()
        pass

    def end_game():
        pass