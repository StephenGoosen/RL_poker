# game_logic.py

import random  as rd
import numpy as np
import itertools

from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator

from game.cards import change_card_str, Deck, change_card_num
import game.config as cg
import game.player as gp
import game.table as tb

agents = cg.agents

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
            try:
                kicker = next(card.rank for card in self.cards if card.rank not in ordered_pairs)
            except StopIteration:
                kicker = None

            return {"hand_type": "Two Pair", "cards": ordered_pairs + [kicker] if kicker is not None else ordered_pairs}

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
    hand_strength = HandEvaluator.evaluate_hand(hole_cards, community_cards)

    # Use Hand to get the hand description
    hand_description = Hand(hole_cards, community_cards).determine_hand()

    # Set hand information for the player
    player.set_hand_info(hand_strength, hand_description['hand_type'])

    # Return the score and hand results
    return hand_strength, hand_description

class GameLogic:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.pot = 0
        self.current_bet = 0
        self.betting_round_pot = 0

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

        self.players_dealt = False
        self.flop_dealt = False
        self.turn_dealt = False
        self.river_dealt = False
        self.game_over = False

        self.game_states = {
            0: "Pre-Flop",
            1: "Flop",
            2: "Turn",
            3: "River"
        }

        self.game_state = self.game_states[0]

    def rotate_positions(self):
        # Rotate dealer index
        self.dealer_index = (self.dealer_index + 1) % len(self.players)

        # Rotate small blind index
        self.small_blind_index = (self.small_blind_index + 1) % len(self.players)

        # Rotate big blind index
        self.big_blind_index = (self.big_blind_index + 1) % len(self.players)

        # Rotate active player index
        self.active_player_index = (self.active_player_index + 1) % len(self.players)

    def new_round(self):
        # Resets the game state for a new round
        # Resets Deck
        # Shuffles Deck
        # Rotates small and big blind and dealer
        # Sets active player
        self.deck = Deck()
        self.deck.shuffle()
        self.rotate_positions()

    def deal_hole_cards(self):
        for player in self.players:
            if player.game_in_play:
                player.hand.append(self.deck.deal_card())

        for player in self.players:
            if player.game_in_play:
                player.hand.append(self.deck.deal_card())
        
        self.players_dealt = True

    def highest_bet(self):
        highest_bet = 0
        for player in self.players:
            if player.bet > highest_bet:
                highest_bet = player.bet
        return highest_bet

    def betting_round(self, pre_flop=False):
        '''
        Betting round function
        '''
        # Get the players in play and in game
        active_player_index = self.active_player_index

        if pre_flop:
            highest_bet = 2
        else:
            highest_bet = 0

        round_finished = False

        while not round_finished:
            current_player = self.players[active_player_index]
            
            if current_player.game_in_play == False:
                print(f"{current_player.name} is out of the game.")

            elif current_player.all_in:
                print(f"{current_player.name} is all-in.")

            elif current_player.folded:
                print(f"{current_player.name} has folded.")

            elif current_player.round_played == False or current_player.bet < self.highest_bet():

                # Let the player choose their action
                action = self.get_player_action(current_player, highest_bet)

                if action == '0':
                    self.check_call(current_player, highest_bet)
                elif action == '1':
                    self.bet_raise(current_player, highest_bet)
                elif action == '2':
                    self.fold(current_player)
                else:
                    print("Invalid action. Please choose from 1(check_call), 2(bet_raise), or 3(fold).")
                    continue

                current_player.round_played = True
                highest_bet = self.highest_bet()

            active_player_index = (active_player_index + 1) % len(self.players)

            # Check if all active players have matched the highest bet or gone all-in or folded
            round_finished = all(
                not player.game_in_play or player.all_in or player.folded or (
                    (player.bet == highest_bet and player.round_played)
                )
                for player in self.players
            )

        self.pot += self.betting_round_pot
        self.betting_round_pot = 0

        # Reset betting variables for all players still in the game
        for player in self.players:
            player.reset_betting()

        print("Betting round finished.")


    def get_player_action(self, player, highest_bet):
        if highest_bet == 0:
            options = "0 1 2"
        else:
            options = "0 1 2"

        try:
            action = input(f"{player.name}, choose your action (Check(0), Bet/Raise(1), Fold(2)): ")
        except ValueError:
            print("Invalid input. Please enter a valid action.")
            return self.get_player_action(player, highest_bet)

        if action not in options.split():
            print("Invalid action. Please choose a valid action.")
            return self.get_player_action(player, highest_bet)

        return action

    def check_call(self, player, highest_bet):
        print(f"Highest bet: {highest_bet}")
        if player.chipcount >= highest_bet:
            bet_amount = (highest_bet - player.bet)
            print(f"{player.name} checks/calls with {bet_amount} chips.")
        else:
            bet_amount = player.chipcount
            print(f"{player.name} is all-in with {bet_amount} chips.")

        player.bet += bet_amount
        player.chipcount -= bet_amount

        if player.chipcount == 0:
            player.all_in = True

        self.betting_round_pot += bet_amount

    def bet_raise(self, player, highest_bet):
        try:
            bet_amount = int(input(f"{player.name}, enter your bet amount (current highest bet: {highest_bet}): "))
        except ValueError:
            print("Invalid input. Please enter a valid bet amount.")
            return self.bet_raise(player, highest_bet)

        # Validate the bet amount
        if (bet_amount + player.bet) < highest_bet or bet_amount > player.chipcount:
            print("Invalid bet amount. Please enter a valid amount within the allowed range.")
            return self.bet_raise(player, highest_bet)

        # Process the bet raise
        player.bet += bet_amount
        player.chipcount -= bet_amount
        
        if player.chipcount == 0:
            player.all_in = True
        
        self.betting_round_pot += bet_amount

        return bet_amount
    
    def fold(self, player):
        print(f"{player.name} folds.")
        player.folded = True


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
    
    def update_active_players(self):
        # Update the active player indices to skip players who are out of the game
        active_player_indices = [i for i, player in enumerate(self.players) if player.game_in_play]
        return active_player_indices

    def blinds(self):
        # Update the active player indices
        active_player_indices = self.update_active_players()

        # Small blind
        for i in active_player_indices:
            player = self.players[i]
            if i == active_player_indices[0]:
                self.pot += cg.small_blind
                player.chipcount -= cg.small_blind
                player.bet += cg.small_blind
                print(f"{player.name} posts the small blind of {cg.small_blind} chips.")

        # Big blind
        for i in active_player_indices:
            player = self.players[i]
            if i == active_player_indices[1]:
                self.pot += cg.big_blind
                player.chipcount -= cg.big_blind
                player.bet += cg.big_blind
                print(f"{player.name} posts the big blind of {cg.big_blind} chips.")

    def pre_flop(self, pre_flop=True):
        self.update_active_players()
        self.blinds()
        self.betting_round()

    def flop(self):
        self.deck.deal_card()  # burn card
        self.flop_cards = [self.deck.deal_card() for _ in range(3)]
        self.community_cards.insert_flop(self.flop_cards)
        return True, self.flop_cards

    def pre_turn(self, pre_flop=False):
        self.betting_round()
        pass

    def turn(self):
        self.deck.deal_card()  # burn card
        self.turn_card = self.deck.deal_card()
        self.community_cards.insert_turn(self.turn_card)
        return True, self.turn_card

    def pre_river(self, pre_flop=False):
        self.betting_round()
        pass

    def river(self):
        self.deck.deal_card()  # burn card
        self.river_card = self.deck.deal_card()
        self.community_cards.insert_river(self.river_card)
        return True, self.river_card

    def showdown(self, pre_flop=False):
        self.betting_round()
        pass

    def winner_winner(self):
        # Get a list of players eligible for winning
        players_eligible = []
        for player in self.players:
            if player.folded == False:
                players_eligible.append(player)

        # Sort the players by hand strength)
        sorted_players = sorted(players_eligible, key=lambda player: player.hand_strength, reverse=True)

        # Find the winner(s)
        winning_players = [sorted_players[0]]
        max_hand_strength = sorted_players[0].hand_strength

        for player in sorted_players[1:]:
            if player.hand_strength == max_hand_strength:
                winning_players.append(player)
            else:
                break

        # Handle tie and split the pot evenly
        if len(winning_players) > 1:
            # Split the pot evenly among tied players
            share_of_pot = self.pot / len(winning_players)
            for winner in winning_players:
                winner.chipcount += share_of_pot
        else:
            # Only one winner, give them the entire pot
            winning_players[0].chipcount += self.pot

    def end_round(self):

        self.winner_winner()
        # Check if any players are out of the game
        still_in_game = 0
        self.winner = []
        for player in self.players:
            if player.chipcount == 0:
                player.game_in_play = False
            if player.game_in_play:
                self.winner.append(player)
                still_in_game += 1
        print(still_in_game)
        if still_in_game <= 1:
            self.end_game()
            pass

        self.community_cards.reset()
        self.pot = 0
        self.current_bet = 0
        self.players_dealt = False
        self.flop_dealt = False
        self.turn_dealt = False
        self.river_dealt = False
        self.cards_dealt = False
        for player in self.players:
                player.reset_round()

    def end_game(self):
        print("Game over!")
        print(f"{self.winner[0].name} wins!")
        self.__init__()
        pass