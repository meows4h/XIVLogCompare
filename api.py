from config import CLIENT_ID, CLIENT_SECRET
from fflogsapi import FFLogsClient, GQLEnum


client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)


def pull_player(info, player, idx):
    ''''''
    for entry in info[idx]:
        if player in entry.values():
            return entry


def get_player_data(rid, number, player):
    ''''''
    report = client.get_report(rid)
    fight = report.fight(number)
    damage = fight.events({"dataType": GQLEnum("DamageDone")})
    casts = fight.events({"dataType": GQLEnum("Casts")})
    summary = fight.table({"dataType": GQLEnum("Summary")})
    events = fight.events({"dataType": GQLEnum("All")})
    
    print(casts)
    print(damage)
    #print(events)

    data = {}

    data["damage"] = pull_player(damage, player, "entries")
    data["casts"] = pull_player(casts, player, "entries")
    data["time"] = summary["totalTime"] 

    return data


def compare_casts(cast_name, x, y):
    ''''''


req_logs = [["kNn2rcQKLZCTgHdh", 46, "Meows For'heals"], ["hdzNJKTx8Grv9tAY", 3, "Mindy Ciao"]]
cast_data = []

for req in req_logs:
    cast_data.append(get_player_data(req[0], req[1], req[2]))

print(cast_data[1])

client.close()
client.save_cache()
