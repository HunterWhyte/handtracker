from tinydb import TinyDB, Query
import plotly.graph_objects as go



handdb = TinyDB("handdb.json")  # initialize DB

tournamentdb = TinyDB("tournamentdb.json")

net = [0]
showdown = [0]
nonshowdown = [0]
allinev = [0]
conversion = 1 # 0.00043 for 0.23 0.2 rake
for i in handdb.all():
    if True:   # filters
        if i["showdown"] == True:
            showdown.append(showdown[-1] + i["net"]*conversion)
            nonshowdown.append(nonshowdown[-1])
            print("showdown:        net: " + str(i["net"]) + "    cev:" + str(i["cev"]))
        else:
            print("non-showdown:    net: " + str(i["net"]) + "    cev:" + str(i["cev"]))
            showdown.append(showdown[-1])
            nonshowdown.append(nonshowdown[-1] + i["net"]*conversion)

        allinev.append(allinev[-1] + i["cev"]*conversion)
        net.append(net[-1] + i["net"]*conversion)

print(len(tournamentdb.all()))
fig = go.Figure()
fig.add_trace(go.Scatter(y=net,
                    mode='lines',
                    name='net'))
fig.add_trace(go.Scatter(y=showdown,
                    mode='lines',
                    name='showdown'))
fig.add_trace(go.Scatter(y=nonshowdown,
                    mode='lines',
                    name='nonshowdown'))
fig.add_trace(go.Scatter(y=allinev,
                    mode='lines',
                    name='all-in ev'))

fig.show()