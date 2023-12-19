# game_logic.py

from itertools import combinations

from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator

from game.cards import change_card_str

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

                # Check if there is a sequence of five consecutive ranks, considering A-2-3-4-5
                for i in range(len(ordered) - 4):
                    if all(ordered[i + j].rank == (ordered[i].rank + j) % 14 + 1 for j in range(5)):
                        return {"hand_type": "Straight Flush", "cards": [card.rank for card in ordered[i:i + 5]]}

                # Check for the special case of A-2-3-4-5 straight flush
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
        # Check for Three of a Kind
        for rank in set(card.rank for card in self.cards):
            rank_cards = [card for card in self.cards if card.rank == rank]
            if len(rank_cards) == 3:
                other_cards = [card for card in self.cards if card.rank != rank]
                return {"hand_type": "Three of a Kind", "cards": [card.rank for card in rank_cards] + [other_cards[0].rank, other_cards[1].rank]}

        return None

    def two_pair(self):
        # Create a dictionary to store the count of each rank
        rank_counts = {}
        for card in self.cards:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1

        # Extract ranks with count 2 (pairs)
        pairs = [rank for rank, count in rank_counts.items() if count == 2]

        if len(pairs) >= 2:
            # Sort pairs in descending order
            ordered_pairs = sorted(pairs, reverse=True)
            
            # Find the remaining card (kicker)
            kicker = next(card.rank for card in self.cards if card.rank not in ordered_pairs)

            return {"hand_type": "Two Pair", "cards": ordered_pairs + [kicker]}

        return None

    def one_pair(self):
        # collect pairs
        pairs = [rank for rank in set(self.ranks) if self.ranks.count(rank) == 2]

        # if there's exactly one pair
        if len(pairs) == 1:
            # Collect other unique ranks in descending order
            unique_ranks = sorted(set(self.ranks) - set(pairs), reverse=True)
            
            return {"hand_type": "One Pair", "cards": pairs + unique_ranks[:3]}

        return None

    def high_card(self):
        # Sort the cards in descending order
        ordered_cards = sorted(self.cards, key=lambda card: card.rank, reverse=True)

        # Return the rank of the highest card
        return {"hand_type": "High Card", "cards": [ordered_cards[0].rank]}


    def determine_hand(self):
        # Check for a Royal Flush
        royal_flush_result = self.royal_flush()
        if royal_flush_result:
            return royal_flush_result

        # Check for a Straight Flush
        straight_flush_result = self.straight_flush()
        if straight_flush_result:
            return straight_flush_result

        # Check for Four of a Kind
        four_of_a_kind_result = self.four_of_a_kind()
        if four_of_a_kind_result:
            return four_of_a_kind_result

        # Check for a Full House
        full_house_result = self.full_house()
        if full_house_result:
            return full_house_result

        # Check for a Flush
        flush_result = self.flush()
        if flush_result:
            return flush_result

        # Check for a Straight
        straight_result = self.straight()
        if straight_result:
            return straight_result

        # Check for Three of a Kind
        three_of_a_kind_result = self.three_of_a_kind()
        if three_of_a_kind_result:
            return three_of_a_kind_result

        # Check for Two Pair
        two_pair_result = self.two_pair()
        if two_pair_result:
            return two_pair_result

        # Check for One Pair
        one_pair_result = self.one_pair()
        if one_pair_result:
            return one_pair_result

        # If none of the above, it's a High Card
        high_card_result = self.high_card()
        return high_card_result

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