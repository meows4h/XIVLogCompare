import math

class Pictomancer:
    def __init__(self, int_stat, crit_stat, dh_stat, det_stat):
        
        intel = int_stat
        crit = crit_stat
        dh = dh_stat
        det = det_stat

        # add a 2nd idx CDH marker later
        # honestly also flip these to be ids -> data
        # not names -> ids -> data
        skills = {
            "Aero in Green": [34651, 530],
            "Attack": [7, 1],
            "Blizzard in Cyan": [34653, 860],
            "Clawed Muse": [34672, 800, 0.7],
            "Comet in Black": [34663, 940, 0.65],
            "Fanged Muse": [34673, 800, 0.7],
            "Fire in Red": [34650, 490],
            "Hammer Brush": [34679, 580, 0.7],
            "Hammer Stamp": [34678, 560, 0.7],
            "Holy in White": [34662, 570, 0.65],
            "Mog of the Ages": [34676, 1000, 0.7],
            "Polishing Hammer": [34680, 600, 0.7],
            "Pom Muse": [34670, 800, 0.7],
            "Rainbow Drip": [34688, 1000, 0.85],
            "Retribution of the Madeen": [34677, 1100, 0.7],
            "Star Prism": [34681, 1100, 0.7],
            "Stone in Yellow": [34654, 900],
            "Thunder in Magenta": [34655, 940],
            "Water in Blue": [34652, 570],
            "Winged Muse": [34671, 800, 0.7]
        }

        buffs = raidbuffs["Starry Muse"]

        


def process_cdhrate(rate, dmg, dot):
    ''''''
    base_rate = 0.25 # need to figure this one out
    crit_boost = 1.4 + (base_rate - 0.05)

    if not dot:
        crit_dmg = (math.log(crit_boost) / math.log(crit_boost * 1.25)) * (dmg - (dmg / crit_boost * 1.25))
        direct_dmg = (math.log(1.25) / math.log(crit_boost * 1.25)) * (dmg - (dmg / crit_boost * 1.25))


# reverse all dictionaries when not on vim
# ALSO add the buff % and type
targetbuffs = {
    "Chain Stratagem": 1001221,
    "Vulnerability Down": 1002198,
}

def targetbuff_ids():
    ''''''
    return {v: k for k, v in targetbuffs.items()}

def process_targetbuffs(ids, dmg, dot):
    ''''''
    targetbuffs = targetbuff_ids()
    base_dmg = dmg

    for buff in ids:
        name = targetbuffs[buff]
        if name == "Chain Stratagem":
            # 10% crit rate
            base_dmg = process_cdhrate(0.1, base_dmg, dot)        
        elif name == "Dokumori":
            # 5% dmg
            base_dmg /= 1.05

    return base_dmg

raidbuffs = {
    "Arcane Circle": 1002599,
    "Army's Paeon": 1002218,
    "Battle Voice": 1000141,
    "Mage's Ballad": 1002217,
    "Medicated": 1000049,
    "Radiant Finale": 1002964,
    "Starry Muse": 1003685,
    "The Wanderer's Minuet": 1002216,
    "Battle Litany": 1000786,
    "Brotherhood": 1001185,
    "Devilment": 1001825,
    "Divination": 1001878,
    "Standard Finish": 1002105,
    "Technical Finish": 1001822,
    "The Spear": 1003889
}

def raidbuff_ids():
    ''''''
    return {v: k for k, v in raidbuffs.items()}

def process_raidbuffs(ids, dmg):
    ''''''
    raidbuffs = raidbuff_ids()
    base_dmg = dmg

    for buff in ids:
        name = raidbuffs[buff]
        if name == "Arcane Circle":
            # 3% dmg
            base_dmg /= 1.03
        elif name == "Battle Litany":
            # 10% crit rate
            print("idk")
        elif name == "Battle Voice":
            # 20% direct
            print("idk")
        elif name == "Brotherhood":
            # 5% dmg
            base_dmg /= 1.05
        elif name == "Divination":
            # 6% dmg
            base_dmg /= 1.06
        elif name == "Embolden":
            # 5% dmg
            base_dmg /= 1.05
        elif name == "Searing Light":
            # 5% dmg
            base_dmg /= 1.05
        elif name == "Radiant Finale":
            # 2-6% dmg what does that mean
            base_dmg /= 1.06
        elif name == "Starry Muse":
            # 5% dmg
            base_dmg /= 1.05
        elif name == "Technical Finish":
            # 1-5% dmg but let's bfr
            base_dmg /= 1.05

    return base_dmg



