allcards = ['as', 'ks', 'qs', 'js', 'ts', '9s', '8s', '7s', '6s', '5s', '4s', '3s', '2s', 'ah', 'kh', 'qh', 'jh', 'th', '9h', '8h', '7h', '6h', '5h', '4h', '3h', '2h', 'ad', 'kd', 'qd', 'jd', 'td', '9d', '8d', '7d', '6d', '5d', '4d', '3d', '2d', 'ac', 'kc', 'qc', 'jc', 'tc', '9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c']
possiblehands = []
for x in range(len(allcards)):
    for y in range(x + 1, len(allcards)):
        hand = [allcards[x], allcards[y]]
        possiblehands.append(hand)
allmatchups = []
for i in range(len(possiblehands)):
    for j in range(i + 1, len(possiblehands)):
        matchup = possiblehands[i][0], possiblehands[i][1], possiblehands[j][0], possiblehands[j][1]
        cardsinplay = [possiblehands[i][0], possiblehands[i][1], possiblehands[j][0], possiblehands[j][1]]
        count = [cardsinplay.count(x) for x in cardsinplay]
        if max(count) == 1:
            allmatchups.append(matchup)

preflopLUT = {}
f = open("matchups.txt", "r")
matchups = f.read().rstrip().split("\n")
f.close()
for i in range(len(matchups)):
    matchups[i] = tuple(matchups[i].split(" "))
for i in range(len(allmatchups)):
    preflopLUT[allmatchups[i]] = matchups[i]
    # 1712304 total matches


def preflop(h1c1, h1c2, h2c1, h2c2):
    # generate preflop LUT
    # order of hands
    h = 1
    if (h1c1, h1c2, h2c1, h2c2) in preflopLUT:
        hand = (h1c1, h1c2, h2c1, h2c2)
    elif (h1c1, h1c2, h2c2, h2c1) in preflopLUT:
        hand = (h1c1, h1c2, h2c2, h2c1)

    elif (h1c2, h1c1, h2c1, h2c2) in preflopLUT:
        hand = (h1c2, h1c1, h2c1, h2c2)
    elif (h1c2, h1c1, h2c2, h2c1) in preflopLUT:
        hand = (h1c2, h1c1, h2c2, h2c1)

    elif (h2c1, h2c2, h1c1, h1c2) in preflopLUT:
        hand = (h2c1, h2c2, h1c1, h1c2)
        h=2
    elif (h2c1, h2c2, h1c2, h1c1) in preflopLUT:
        hand = (h2c1, h2c2, h1c2, h1c1)
        h=2

    elif (h2c2, h2c1, h1c1, h1c2) in preflopLUT:
        hand = (h2c2, h2c1, h1c1, h1c2)
        h=2
    elif (h2c2, h2c1, h1c2, h1c1) in preflopLUT:
        hand = (h2c2, h2c1, h1c2, h1c1)
        h=2
    else:
        print("matchup not found")
        print(h1c1, h1c2, h2c1, h2c2)
        return 0,0
    result = preflopLUT[hand]
    if h == 1:
        winsper = 100 * float(result[0]) / 1712304
        tiesper = 100 * float(result[1]) / 1712304
    else:
        winsper = 100 - (100 * float(result[0]) / 1712304)
        tiesper = 100 * float(result[1]) / 1712304
    return winsper, tiesper