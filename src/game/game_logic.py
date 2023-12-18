# game_logic.py

from itertools import combinations

from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator

def hand_ranking(hole_cards, community_cards):
    cards = hole_cards + community_cards

    values = [card.rank for card in cards]
    suits = [card.suit for card in cards]

    # Check for flush
    flush = len(set(suits)) == 1

    # Check for straight
    straight = (
        (values[0] - values[4] == 4 and len(set(values)) == 5) or
        (values[1] == 5 and values[0] == 14 and len(set(values[1:])) == 4)
    )

    # Check for royal flush
    if straight and flush and values[0] == 14:
        return 9, "Royal Flush"

    # Check for straight flush
    if straight and flush:
        return 8, "Straight Flush"

    # Check for four of a kind
    if values.count(values[0]) == 4 or values.count(values[1]) == 4:
        return 7, "Four of a Kind"

    # Check for full house
    if values.count(values[0]) == 3 and values.count(values[4]) == 2:
        return 6, "Full House"
    elif values.count(values[0]) == 2 and values.count(values[4]) == 3:
        return 6, "Full House"

    # Check for flush
    if flush:
        return 5, "Flush"

    # Check for straight
    if straight:
        return 4, "Straight"

    # Check for three of a kind
    if values.count(values[0]) == 3 or values.count(values[2]) == 3 or values.count(values[4]) == 3:
        return 3, "Three of a Kind"

    # Check for two pair
    if len(set(values)) == 3 and (values.count(values[0]) == 2 or values.count(values[2]) == 2 or values.count(values[4]) == 2):
        return 2, "Two Pair"

    # Check for one pair
    if len(set(values)) == 4:
        return 1, "One Pair"

    # High card
    return 0, "High Card"


def compare_scores(score_dict):
    # Hand dict has the player name and the players score

    # Loop through each
    player_scores = {}
    for name, score in score_dict:
        player_scores[name] = score
        #sort by score and return highest score/scores
        sorted_scores = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[0][0]

def hand_evaluation(hole_cards, community_cards):

    score = HandEvaluator.evaluate_hand(hole_cards, community_cards)
    ranking = hand_ranking(hole_cards, community_cards)
    return score, ranking[1]