from itertools import combinations

def hand_ranking(cards):
    values = sorted([int(card[0]) if card[0] != 'A' else 1 for card in cards], key=lambda x: x)
    suits = [card[1] for card in cards]

    straight = (max(values) - min(values) == 4) and (len(set(values)) == 5)
    flush = len(set(suits)) == 1

    # Check for straight flush
    if straight and flush:
        return 8, values

    # Check for four of a kind
    if len(set(values)) == 2 and values.count(values[0]) in [1, 4]:
        return 7, values

    # Check for full house
    if len(set(values)) == 2 and values.count(values[0]) in [2, 3]:
        return 6, values

    # Check for flush
    if flush:
        return 5, values

    # Check for straight
    if straight:
        return 4, values

    # Check for three of a kind
    if len(set(values)) == 3 and 3 in [values.count(x) for x in set(values)]:
        return 3, values

    # Check for two pairs
    if len(set(values)) == 3 and 2 in [values.count(x) for x in set(values)]:
        return 2, values

    # Check for one pair
    if len(set(values)) == 4 and 2 in [values.count(x) for x in set(values)]:
        return 1, values

    # High card
    return 0, values

def evaluate_hand(hole_cards, community_cards):
    all_cards = hole_cards + community_cards
    all_combinations = list(combinations(all_cards, 5))

    best_rank = (0, [])

    for combination in all_combinations:
        values = sorted([str(card.value) for card in combination], key=lambda x: (x if x != 'A' else '1'))
        suits = [card.suit for card in combination]

        rank = hand_ranking(list(zip(values, suits)))
        if rank > best_rank:
            best_rank = rank
            best_combination = combination

    return best_rank, best_combination 