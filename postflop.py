from joblib import Parallel, delayed
import itertools as iter


def seven_card(h1,h2):
    # params: seven card poker hands
    h1options = [list(x) for x in iter.combinations(h1, 5)]
    h2options = [list(x) for x in iter.combinations(h2, 5)]
    blank, hand1 = poker(h1options)
    blank, hand2 = poker(h2options)
    result, hand = poker([hand1, hand2])
    if result == 0:
        return 2
    elif result == 1:
        return hand == hand1

def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    result = [x for x in hands if hand_rank(x) == hand_rank(max(hands, key=hand_rank))]
    if len(result) > 1:
        return 0, result[0]
    else:
        return 1, result[0]

def hand_rank(hand):
    groups = group(["--23456789tjqka".index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14,5,4,3,2):
        ranks = (5,4,3,2,1)
    straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
    flush = len(set([s for r,s in hand])) == 1
    return max(count_rankings[counts], 4*straight +5*flush), ranks
count_rankings = {(5,):10,
                  (4,1):7,
                  (3,2):6,
                  (3,1,1):3,
                  (2,2,1):2,
                  (2,1,1,1):1,
                  (1,1,1,1,1):0}
def group(items):
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse=True)
def unzip(pairs):
    return zip(*pairs)

def winloss(h1,h2,communities):
    ties=0
    wins=0
    results = Parallel(n_jobs=-1)(delayed(seven_card)(h1 + i, h2 + i)for i in communities)
    for result in results:
        if result == 2:
            ties += 1
        elif result == 1:
            wins += 1
    return wins, ties
# def winlossnonp(h1,h2,communities):
#     ties=0
#     wins=0
#     results = (seven_card(h1 + i, h2 + i)for i in communities)
#     for result in results:
#         if result == 2:
#             ties += 1
#         elif result == 1:
#             wins += 1
#     return wins, ties