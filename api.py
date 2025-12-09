from config import CLIENT_ID, CLIENT_SECRET
from jobref import pct_ids, pictomancer
from fflogsapi import FFLogsClient, GQLEnum


client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)


def get_pid(name, fight):
    ''''''
    for player in fight.player_details():
        if player.name == name:
            return player.id


def get_events(fight, cat, pid):
    ''''''
    return fight.events({"dataType": GQLEnum(cat),
                         "sourceID": pid})


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
    damage = get_events(fight, "DamageDone", pid)
    # casts = get_events(fight, "Casts")
    duration = fight.duration()
    encounter = fight.encounter().name()

    # graph_test = fight.table({"dataType": GQLEnum("Casts")})

    void_id = -1
    if encounter == "Futures Rewritten":
        void_id = get_fru_void(fight)

    pct_id = pct_ids()
    dmg_count = {}
    mode = "damage"

    print(damage)

    for idx in damage:
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

    return dmg_count


def add_plus(var):
    ''''''
    if var > 0:
        return f'+{var}'
    else:
        return f'{var}'


def compare_casts(name, spells):
    ''''''
    output = f'{name}'
    while len(output) < 28:
        output += ' '

    output += ': '
    for spell in spells:
        temp = f'{spell[0]}'
        if len(temp) == 1:
            temp += ' '
        temp += f' ({spell[1]})'
        while len(temp) < 18:
            temp += ' '
        output += temp

    cast_diff = spells[0][0] - spells[1][0]
    damage_diff = spells[0][1] - spells[1][1]

    cast_disp = add_plus(cast_diff)
    dmg_disp = add_plus(damage_diff)
    output += f' | {cast_disp} ({dmg_disp})'

    print(output)
    return damage_diff


req_logs = [["kNn2rcQKLZCTgHdh", 46, "Meows For'heals"], ["hdzNJKTx8Grv9tAY", 3, "Mindy Ciao"]]
cast_data = []

title_out = ''
while len(title_out) < 30:
    title_out += ' '

for req in req_logs:
    cast_data.append(get_player_data(req[0], req[1], req[2]))
    temp = req[2]
    while len(temp) < 18:
        temp += ' '
    title_out += temp

print(title_out)

total_dmg = 0
for meow in pictomancer:
    spells = []
    for index in cast_data:
        spells.append(index[meow])
    total_dmg += compare_casts(meow, spells)

final_out = ''
while len(final_out) < 69:
    final_out += ' '
final_out += f'{total_dmg}'
print(final_out)

# use duration to parse into dps number
# figure out which buff ids are which, remove additional external buffs

client.close()
client.save_cache()
