from tinydb import TinyDB, Query

handdb = TinyDB("handdb.json")  # initialize DB

tournamentdb = TinyDB("tournamentdb.json")

for i in handdb.all():
    if i["showdown"] == True:
        print("showdown:        net: " + str(i["net"]) + "    cev:" + str(i["cev"]))
    else:
        print("non-showdown:    net: " + str(i["net"]) + "    cev:" + str(i["cev"]))
