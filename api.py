from config import CLIENT_ID, CLIENT_SECRET
from jobref import pct_ids
from fflogsapi import FFLogsClient, GQLEnum


client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)


def get_pid(name, fight):
    ''''''
    for player in fight.player_details():
        if player.name == name:
            return player.id


def get_events(fight, cat):
    ''''''
    return fight.events({"dataType": GQLEnum(cat)})


def get_fru_void(fight):
    ''''''
    enemies = fight.enemy_npcs()
    for enemy in enemies:
        if enemy.game_id == 17828:
            return enemy.id


def get_player_data(rid, number, player):
    ''''''
    report = client.get_report(rid)
    fight = report.fight(number)
    pid = get_pid(player, fight)
    damage = get_events(fight, "DamageDone")
    # casts = get_events(fight, "Casts")
    duration = fight.duration()
    encounter = fight.encounter().name()

    void_id = -1
    if encounter == "Futures Rewritten":
        void_id = get_fru_void(fight)

    player_damage = []

    for idx in damage:
        if "sourceID" in idx:
            if idx["sourceID"] == pid:
                player_damage.append(idx)

    pct_id = pct_ids()
    dmg_count = {}
    # mode = "calculateddamage"
    mode = "damage"

    for idx in player_damage:
        if "abilityGameID" in idx and idx["type"] == mode:

            if idx["targetID"] == void_id:
                continue

            cid = idx["abilityGameID"]
            if cid in pct_id:

                cast_name = pct_id[cid]
                if cast_name in dmg_count:
                    dmg_count[cast_name][0] += 1
                    dmg_count[cast_name][1] += idx["amount"]
                else:
                    dmg_count[cast_name] = [1, idx["amount"]]

    print(dmg_count)

    data = {}

    return data


def compare_casts(cast_name, x, y):
    ''''''


req_logs = [["kNn2rcQKLZCTgHdh", 46, "Meows For'heals"], ["hdzNJKTx8Grv9tAY", 3, "Mindy Ciao"]]
cast_data = []

for req in req_logs:
    cast_data.append(get_player_data(req[0], req[1], req[2]))

# use duration to parse into dps number
# figure out which buff ids are which, remove additional external buffs

client.close()
client.save_cache()
