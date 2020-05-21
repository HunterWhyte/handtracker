import time
from preflop import *
from postflop import *
allcards = ['as', 'ks', 'qs', 'js', 'ts', '9s', '8s', '7s', '6s', '5s', '4s', '3s', '2s', 'ah', 'kh', 'qh', 'jh', 'th', '9h', '8h', '7h', '6h', '5h', '4h', '3h', '2h', 'ad', 'kd', 'qd', 'jd', 'td', '9d', '8d', '7d', '6d', '5d', '4d', '3d', '2d', 'ac', 'kc', 'qc', 'jc', 'tc', '9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c']

def holdem_odds(h1c1, h1c2,h2c1, h2c2, fc1, fc2, fc3, tc, rc):
    cards = [h1c1, h1c2,h2c1, h2c2, fc1, fc2, fc3, tc, rc]
    cards = [x.lower() for x in cards]
    knowncards = [x for x in cards if x != ""]
    h1c1 = h1c1.lower()
    h1c2 = h1c2.lower()
    h2c1 = h2c1.lower()
    h2c2 = h2c2.lower()
    fc1 = fc1.lower()
    fc2 = fc2.lower()
    fc3 = fc3.lower()
    tc = tc.lower()
    rc = rc.lower()

    cardsinplay = allcards.copy()
    for i in knowncards:
        cardsinplay.remove(i)
    if fc1 == "":
        return preflop(h1c1, h1c2, h2c1, h2c2)

    elif tc == "":
        communities = [list(x) for x in (iter.combinations(cardsinplay, 2))]
        h1 = [h1c1, h1c2, fc1, fc2, fc3]
        h2 = [h2c1, h2c2, fc1, fc2, fc3]
        wins,ties = winloss(h1,h2,communities)
        winper = wins/ len(communities)
        tiesper = ties / len(communities)
        return winper*100, tiesper*100
    elif rc == "":
        communities = [[x] for x in cardsinplay]
        h1 = [h1c1, h1c2, fc1, fc2, fc3, tc]
        h2 = [h2c1, h2c2, fc1, fc2, fc3, tc]
        wins,ties = winloss(h1,h2,communities)
        winper = wins / len(communities)
        tiesper = ties / len(communities)
        return winper*100, tiesper*100
    else:
        h1 = [h1c1, h1c2, fc1, fc2, fc3, tc, rc]
        h2 = [h2c1, h2c2, fc1, fc2, fc3, tc, rc]
        result = seven_card(h1, h2)
        if result == 2:
            return 0, 100
        elif result == 1:
            return 100, 0
        else:
            return 0,0
    return 0
