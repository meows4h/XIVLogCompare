from config import CLIENT_ID, CLIENT_SECRET
from fflogsapi import FFLogsClient
import classes as cl

client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)

req_logs = [["kNn2rcQKLZCTgHdh", 46, "Meows For'heals"], ["hdzNJKTx8Grv9tAY", 3, "Mindy Ciao"]]

compare_instance = cl.Instance()
for req in req_logs:
    rid = req[0]
    num = req[1]
    player_name = req[2]

    report = client.get_report(rid)
    fight_report = report.fight(num)
    fight = cl.Fight(fight_report, player_name)
    compare_instance.add_fight(fight)

for fight in compare_instance.fights:
    print(fight.casts)

compare_instance.print_compare()

client.close()
client.save_cache()
