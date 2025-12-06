from config import CLIENT_ID, CLIENT_SECRET
from fflogsapi import FFLogsClient, GQLEnum


client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)


def get_player_casts(rid, number, player):
    ''''''
    report = client.get_report(rid)
    fight = report.fight(number)
    casts = fight.table({"dataType": GQLEnum("Casts")})
    for entity in casts["entries"]:
        if player in entity.values():
            return entity

    return None


def compare_casts(cast_name, x, y):
    ''''''


req_logs = [["kNn2rcQKLZCTgHdh", 46, "Meows For'heals"], ["hdzNJKTx8Grv9tAY", 3, "Mindy Ciao"]]
cast_data = []

for req in req_logs:
    cast_data.append(get_player_casts(req[0], req[1], req[2]))

print(cast_data[1]["abilities"])

client.close()
client.save_cache()
