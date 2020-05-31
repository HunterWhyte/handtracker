from datetime import datetime
from tinydb import TinyDB, Query
import time
from odds import holdem_odds
def time_difference(time1,time2):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    day1 = int(time1[1])
    hour1 = int(time1[2][0:2])
    minute1 = int(time1[2][3:5])
    second1 = int(time1[2][6:])

    day2 = int(time2[1])
    hour2 = int(time2[2][0:2])
    minute2 = int(time2[2][3:5])
    second2 = int(time2[2][6:])
    totalseconds1 = hour1*3600 + minute1*60 + second1
    totalseconds2 = hour2*3600 + minute2*60 + second2
    if day1 != day2:
        totalseconds2 += 3600*24 #add twenty four hours to second time to account for switchover in days
    difference = (totalseconds2-totalseconds1)
    return (difference)

def parse_action(line):
    amount = 0
    action = "error"
    if line.split()[1] == "is":
        action = "all-in"
    if line.split()[1] == "folds":
        action = "fold"
    if line.split()[1] == "checks":
        action = "check"
    if line.split()[1] == "calls":
        action = "call"
        amount = line.split()[2][1:-1]
    if line.split()[1] == "bets":
        action = "bet"
        amount = line.split()[2][1:-1]
    if line.split()[1] == "raises":
        action = "raise"
        amount = line.split()[2]
    if line.split()[1] == "posts":
        action = "post"
        amount = line.split()[4][1:-1]

    #print(action + ": " + str(amount))
    return action, int(amount)
def twohanded_action(hand):
    # each action has a dictionary type and amount and street
    # initialize variables
    pot = [0]
    playerx = {"name": "", "stack": [], "actions": []}
    hero = {"name": "Hero", "stack": [], "actions": []}
    community = []
    result = "loss"
    showdown = True
    allin = False
    deal = None
    flop = None
    turn = None
    river = None
    summary = None
    lasthand = False
    street = []
    cev = 0
    #print(hand[:2])
    for line in hand[:2]:
        if line.startswith("Seat"):
                if line.split()[2].startswith("Player"):
                    playerx["name"] = line.split()[2]
                    playerx["stack"].append(float(line.split()[3][1:-1]))
                    print(str(playerx["name"]) + str(playerx["stack"]))
                if line.split()[2].startswith("Hero"):
                    hero["stack"].append(float(line.split()[3][1:-1]))
                    print(str(hero["name"]) + str(hero["stack"]))

    for line in hand[2:4]:
        #print("*")
        a = None
    for line in hand[4:]:
        #print(line)
        if line.startswith("** Dealing down cards **"):
            deal = hand.index(line)
        if line.startswith("Dealt to Hero"):
            cards = (line.split()[4][:-1], line.split()[5])
        if line.startswith("** Dealing Flop **"):
            flop = hand.index(line)
            community.append(line.split()[6][:-1])
            community.append(line.split()[7][:-1])
            community.append(line.split()[8])
        if line.startswith("** Dealing Turn **"):
            turn = hand.index(line)
            community.append(line.split()[6])
        if line.startswith("** Dealing River **"):
            river = hand.index(line)
            community.append(line.split()[6])
        if line.startswith("** Summary **"):
            summary = hand.index(line)

    if None in [flop,turn,river]:
         showdown = False
         allin = False
         cev = 0
    else:
        for i in range(len(hand)):
            if i >= deal and i < flop: # preflop action
                street.append("preflop")
            elif i >= flop and i < turn:
                street.append("flop")
            elif i >= turn and i < river:
                street.append("turn")
            elif i >= river and i < summary:
                street.append("river")
            else:
                street.append("start")
        for i in range(2,summary):
            if hand[i].startswith(hero["name"]):
                action, amount = parse_action(hand[i])
                if action == "all-in":
                    allin = street[i]
                else:
                    pot.append(pot[-1]+amount)
                    hero["stack"].append(hero["stack"][-1]-amount)
                    hero["actions"].append({"action": action, "amount": amount})

                    if action == "fold":
                        allin = False
                        showdown = False
            elif hand[i].startswith(playerx["name"]):
                action, amount = parse_action(hand[i])
                if action == "all-in":
                    allin = street[i]
                else:
                    pot.append(pot[-1] + amount)
                    playerx["stack"].append(playerx["stack"][-1] - amount)
                    playerx["actions"].append({"action": action, "amount": amount})

                    if action == "fold":
                        allin = False
                        showdown = False
    if allin != False and allin != "river":
        for i in range(summary, len(hand)):
            # TODO: go straight to summary
            for i in range(summary, len(hand)):
                if hand[i].startswith(playerx["name"]):
                    line = hand[i].split()
                    for j in range(len(line)-5):
                        if (line[j]).startswith("]"):
                            villaincards = (line[j-2][:-1], line[j-1])

                if hand[i].startswith(hero["name"]):
                    line = hand[i].split()
                    for j in range(len(line)):
                        if (line[j]).startswith("net"):
                            net = float(line[j + 1][1:-1])
                            result = "win"
                        if (line[j]).startswith("lost"):
                            net = -float(line[j + 1][:-1])
                            result = "loss"
                        if line[2] == "0,":
                            lasthand = True
            if allin == "preflop":
                eq = holdem_odds(cards[0], cards[1], villaincards[0], villaincards[1], "", "", "", "", "")
            elif allin == "flop":
                eq = holdem_odds(cards[0], cards[1], villaincards[0], villaincards[1], community[0], community[1], community[2], "", "")
            elif allin == "turn":
                eq = holdem_odds(cards[0], cards[1], villaincards[0], villaincards[1], community[0], community[1], community[2], community[3], "")
            bet = min(float(hero["actions"][-1]["amount"]), float(playerx["actions"][-1]["amount"]))
            allinpot = min(hero["stack"][0], playerx["stack"][0])
            cev = (eq[0]/100)*(allinpot) - (1- (eq[0]/100) - (eq[1]/100) )*float(bet)
            print(" *** ALL IN *** \n"  +" "+ allin + " bet: " + str(bet) + " pot: " + str(allinpot) + " hero: " + str(cards) + "villain:" + str(villaincards) + "equity:" + str(eq) + "\n*************")
            print(lasthand, cards, net, showdown, allin, cev, result)
            return (lasthand, cards, net, showdown, allin, cev, result)

    elif showdown == True:
        showdown = True
        cev = 0
        for i in range(summary, len(hand)):
            # TODO: go straight to summary
            for i in range(summary, len(hand)):
                if hand[i].startswith(hero["name"]):
                    line = hand[i].split()
                    for j in range(len(line)):
                        if (line[j]).startswith("net"):
                            net = float(line[j + 1][1:-1])
                            result = "win"
                        if (line[j]).startswith("lost"):
                            net = -float(line[j + 1][:-1])
                            result = "loss"
                        if line[2] == "0,":
                            lasthand = True
            print(lasthand, cards, net, showdown, allin, cev, result)
            return (lasthand, cards, net, showdown, allin, cev, result)

    if showdown == False:
        for i in range(summary, len(hand)):
            for i in range(summary, len(hand)):
                if hand[i].startswith(hero["name"]):
                    line = hand[i].split()
                    for j in range(len(line)):
                        if (line[j]).startswith("net"):
                            net = float(line[j + 1][1:])
                            result = "win"
                        if (line[j]).startswith("lost"):
                            net = -float(line[j + 1])
                            result = "loss"
        print(lasthand, cards, net, showdown, allin, cev, result)
        return (lasthand, cards, net, showdown, allin, cev, result)
    # print(hero)
    # print(playerx)
    # print(pot)

def threehanded_action(hand):
    # each action has a dictionary type and amount and street
    # initialize variables
    pot = [0]
    playerx = {"name": "", "stack": [], "actions": []}
    playery = {"name": "", "stack": [], "actions": []}
    hero = {"name": "Hero", "stack": [], "actions": []}
    playersleft = 3
    community = []
    result = "loss"
    showdown = True
    allin = False
    deal = None
    flop = None
    turn = None
    river = None
    summary = None
    lasthand = False
    street = []
    cev = 0
    # print(hand[:2])
    for line in hand[:3]:
        if line.startswith("Seat"):
            if line.split()[2].startswith("Player"):
                if playerx["name"] == "":
                    playerx["name"] = line.split()[2]
                    playerx["stack"].append(float(line.split()[3][1:-1]))
                    print(str(playerx["name"]) + str(playerx["stack"]))
                else:
                    playery["name"] = line.split()[2]
                    playery["stack"].append(float(line.split()[3][1:-1]))
                    print(str(playery["name"]) + str(playery["stack"]))
            if line.split()[2].startswith("Hero"):
                hero["stack"].append(float(line.split()[3][1:-1]))
                print(str(hero["name"]) + str(hero["stack"]))


    for line in hand[4:]:
        # print(line)
        if line.startswith("** Dealing down cards **"):
            deal = hand.index(line)
        if line.startswith("Dealt to Hero"):
            cards = (line.split()[4][:-1], line.split()[5])
        if line.startswith("** Dealing Flop **"):
            flop = hand.index(line)
            community.append(line.split()[6][:-1])
            community.append(line.split()[7][:-1])
            community.append(line.split()[8])
        if line.startswith("** Dealing Turn **"):
            turn = hand.index(line)
            community.append(line.split()[6])
        if line.startswith("** Dealing River **"):
            river = hand.index(line)
            community.append(line.split()[6])
        if line.startswith("** Summary **"):
            summary = hand.index(line)

    if None in [flop, turn, river]:
        showdown = False
        allin = False
        cev = 0
    else:
        for i in range(len(hand)):
            if i >= deal and i < flop:  # preflop action
                street.append("preflop")
            elif i >= flop and i < turn:
                street.append("flop")
            elif i >= turn and i < river:
                street.append("turn")
            elif i >= river and i < summary:
                street.append("river")
            else:
                street.append("start")
        for i in range(2, summary):
            if hand[i].startswith(hero["name"]):
                action, amount = parse_action(hand[i])
                if action == "all-in":
                    allin = street[i]
                else:
                    pot.append(pot[-1] + amount)
                    hero["stack"].append(hero["stack"][-1] - amount)
                    hero["actions"].append({"action": action, "amount": amount})

                    if action == "fold":
                        allin = False
                        showdown = False
            elif hand[i].startswith(playerx["name"]):
                action, amount = parse_action(hand[i])
                if action == "all-in":
                    allin = street[i]
                else:
                    pot.append(pot[-1] + amount)
                    playerx["stack"].append(playerx["stack"][-1] - amount)
                    playerx["actions"].append({"action": action, "amount": amount})

                    if action == "fold":
                        playersleft = playersleft - 1
            elif hand[i].startswith(playery["name"]):
                action, amount = parse_action(hand[i])
                if action == "all-in":
                    allin = street[i]
                else:
                    pot.append(pot[-1] + amount)
                    playery["stack"].append(playery["stack"][-1] - amount)
                    playery["actions"].append({"action": action, "amount": amount})

                    if action == "fold":
                        playersleft = playersleft - 1

    if allin != False and allin != "river" and playersleft == 2:
        if playery["actions"][-1]["action"] == "fold":
            villain = playerx
        else:
            villain = playery
        for i in range(summary, len(hand)):
            # TODO: go straight to summary
            for i in range(summary, len(hand)):
                if hand[i].startswith(villain["name"]):
                    line = hand[i].split()
                    for j in range(len(line) - 5):
                        if (line[j]).startswith("]"):
                            villaincards = (line[j - 2][:-1], line[j - 1])

                if hand[i].startswith(hero["name"]):
                    line = hand[i].split()
                    for j in range(len(line)):
                        if (line[j]).startswith("net"):
                            net = float(line[j + 1][1:-1])
                            result = "win"
                        if (line[j]).startswith("lost"):
                            net = -float(line[j + 1][:-1])
                            result = "loss"
                        if line[2] == "0,":
                            lasthand = True
            if allin == "preflop":
                eq = holdem_odds(cards[0], cards[1], villaincards[0], villaincards[1], "", "", "", "", "")
            elif allin == "flop":
                eq = holdem_odds(cards[0], cards[1], villaincards[0], villaincards[1], community[0], community[1],
                                 community[2], "", "")
            elif allin == "turn":
                eq = holdem_odds(cards[0], cards[1], villaincards[0], villaincards[1], community[0], community[1],
                                 community[2], community[3], "")

            bet = min(float(hero["actions"][-1]["amount"]), float(villain["actions"][-1]["amount"]))
            allinpot = min(hero["stack"][0], villain["stack"][0])
            cev = (eq[0] / 100) * (allinpot) - (1 - (eq[0] / 100) - (eq[1] / 100)) * float(bet)
            print(" *** ALL IN *** \n" + " " + allin + " bet: " + str(bet) + " pot: " + str(allinpot) + " hero: " + str(
                cards) + "villain:" + str(villaincards) + "equity:" + str(eq) + "\n*************")
            print(lasthand, cards, net, showdown, allin, cev, result)
            return (lasthand, cards, net, showdown, allin, cev, result)

    elif showdown == True:
        showdown = True
        cev = 0
        for i in range(summary, len(hand)):
            # TODO: go straight to summary
            for i in range(summary, len(hand)):
                if hand[i].startswith(hero["name"]):
                    line = hand[i].split()
                    for j in range(len(line)):
                        if (line[j]).startswith("net"):
                            net = float(line[j + 1][1:-1])
                            result = "win"
                        if (line[j]).startswith("lost"):
                            net = -float(line[j + 1][:-1])
                            result = "loss"
                        if line[2][:-1] == "0":
                            lasthand = True
            print(lasthand, cards, net, showdown, allin, cev, result)
            return (lasthand, cards, net, showdown, allin, cev, result)

    if showdown == False:
        for i in range(summary, len(hand)):
            for i in range(summary, len(hand)):
                if hand[i].startswith(hero["name"]):
                    line = hand[i].split()
                    for j in range(len(line)):
                        if (line[j]).startswith("net"):
                            net = float(line[j + 1][1:])
                            result = "win"
                        if (line[j]).startswith("lost"):
                            net = -float(line[j + 1])
                            result = "loss"
                        if (line[j]).startswith("didn't"):
                            net = 0
                            result = "even"

        print(lasthand, cards, net, showdown, allin, cev, result)
        return (lasthand, cards, net, showdown, allin, cev, result)
    # print(hero)
    # print(playerx)
    # print(pot)
def parse_file(filepath):
    f = open(filepath)
    hands = f.read().rstrip().split("\n\n\n")
    hands.reverse()
    parse_hands(hands)

def parse_hands(hands):
    handdb = TinyDB("handdb.json") # initialize DB
    #handdb.truncate() # clear entire DB
    tournamentdb  = TinyDB("tournamentdb.json")
    #tournamentdb.truncate() # clear entire DB
    for hand in hands:
        newhand = {}
        hand = hand.split("\n")

        if hand[1].split()[7:10] != ['(SNG', 'JackPot', 'Tournament']:
            print(hand[1].split()[7:10])
            print("not spin & go")
            print(hand)
            continue
        newhand["ID"] = hand[0].split()[5]

        # check for duplicate hand
        if len(handdb.all()) != 0:
            existinghand = Query()
            if len(handdb.search(existinghand.ID == newhand["ID"])) > 0:
                print("duplicate hand... ignoring")
                continue

        print(newhand["ID"]) # print hand ID for debugging purposes

        newhand["TID"] = hand[1].split()[10][1:-1]
        newhand["buyin"] = hand[1].split()[12][1:]
        newhand["rake"] = hand[1].split()[14][1:-1]
        newhand["stakes"] = hand[1].split()[0]
        newhand["time"] = hand[1].split()[17:]
        newhand["players"] = hand[3].split()[5][0]
        if newhand["players"] == "2":
            if hand[6].startswith("Hero"):
                newhand["position"] = "SB"
            elif hand[7].startswith("Hero"):
                newhand["position"] = "BB"

            try:
                lasthand, cards, net, showdown, allin, cev, result = twohanded_action(hand[4:])
            except:
                print("error parsing hand ID: "+ newhand["ID"] +  "  ... skipping")
                continue
        elif newhand["players"] == "3":
            if hand[7].startswith("Hero"):
                newhand["position"] = "SB"
            elif hand[8].startswith("Hero"):
                newhand["position"] = "BB"
            else:
                newhand["position"] = "BU"

            try:
                lasthand, cards, net, showdown, allin, cev, result = threehanded_action(hand[4:])
            except:
                print("error parsing hand ID: "+ newhand["ID"] +  "  ... skipping")
                continue
        newhand["cards"] = cards
        newhand["net"] = net
        newhand["showdown"] = showdown
        newhand["cev"] = cev

        # insert hand into DB
        handdb.insert(newhand)
        # query existing tournament database and check if tournament already exists
        existingTID = Query()
        if (tournamentdb.search(existingTID.TID == newhand["TID"])) == []:
            newtournament = {}
            newtournament["TID"] = newhand["TID"]
            newtournament["handcount"] = 1
            newtournament["buyin"] = newhand["buyin"]
            newtournament["rake"] = newhand["rake"]
            newtournament["time"] = newhand["time"]
            newtournament["result"] = "unfinished"
            newtournament["duration"] = "unfinished"
            if lasthand == True:
                newtournament["duration"] = "0"
                newtournament["result"] = result
                print("END OF TOURNAMENT")
            tournamentdb.insert(newtournament)
        elif len(tournamentdb.search(existingTID.TID == newhand["TID"])) == 1:
            handcount = tournamentdb.search(existingTID.TID == newhand["TID"])[0]["handcount"] + 1
            if lasthand == True:
                print("END OF TOURNAMENT")
                tournamentdb.update({"duration": time_difference(newtournament["time"], newhand["time"])}, existingTID.TID == newhand["TID"])
                tournamentdb.update({"result": result}, existingTID.TID == newhand["TID"])
            tournamentdb.update({"handcount": handcount}, existingTID.TID == newhand["TID"])


        # # calculate end time and determine place
        # duration = time_difference(newtournament["time"], lasttime)# start time - end time in seconds.
        # newtournament["duration"] = duration
        # newtournament["handcount"] = handcount + 1
        # newtournament["buyin"] = newhand["buyin"]
        # newtournament["rake"] = newhand["rake"]
        # print(newtournament) # insert tournament into dataset
        # # create new tournament
        # lastTID = newhand["TID"]
        # newtournament = {"ID": lastTID, "time":newhand["time"]}
        # lasttime = newhand["time"]


start = time.time()
parse_file("may21-may29.txt")
end = time.time() - start
print("\ntotal seconds: " + str(end))
handdb = TinyDB("handdb.json")
print("time per hand: " + str(end/len(handdb.all())))