import math

# leaving off here, fix up these methods, interwork these better
# framework looks like
# instance holds all values, fights get stored as fight objects to have easier method calls
# Players have Jobs, Jobs have Attacks and Buffs, Events can have Buffs that need removals that are associated with Attacks, etc etc
class Fight:
    def __init__(self, report):
        self.report = report

    def get_pid(name, fight):
    ''''''
    for player in fight.player_details():
        if player.name == name:
            return player.id

    def get_events(fight, cat, pid):
        ''''''
        return fight.events({"dataType": GQLEnum(cat),
                             "sourceID": pid})


class Attack:
    def __init__(self, name, pot, dot=False, cd=None, cleave=1):
        self.name = name
        self.potency = pot
        self.dot = dot
        self.cd = cd
        self.cleave = cleave

    def process_cdhrate(rate, dmg, dot):
        ''''''
        base_rate = 0.25 # need to figure this one out
        crit_boost = 1.4 + (base_rate - 0.05)

        if not dot:
            crit_dmg = (math.log(crit_boost) / math.log(crit_boost * 1.25)) * (dmg - (dmg / crit_boost * 1.25))
            direct_dmg = (math.log(1.25) / math.log(crit_boost * 1.25)) * (dmg - (dmg / crit_boost * 1.25))


class Buff:
    def __init__(self, name, percent, bonus="dmg", target=False):
        self.name = name
        self.percent = percent
        self.type = bonus
        self.target = target


class Player:
    def __init__(self, pid):
        self.pid = pid


class Instance:
    def __init__(self, name, pids, duration):
        self.name = name

        self.players = []
        for pid in pids:
            self.players.append(Player(pid))

        self.duration = duration

        self.buffs = {
            1002599: Buff("Arcane Circle", 1.03),
            1002218: Buff("Army's Paeon", 0.03, bonus='direct'),
            1000141: Buff("Battle Voice", bonus='direct'),
            1002217: Buff("Mage's Ballad" 1.01),
            1000049: Buff("Medicated", 1.08),
            1002964: Buff("Radiant Finale", 1.06),
            1003685: Buff("Starry Muse", 1.05),
            1002216: Buff("The Wanderer's Minuet", 0.02, bonus='crit'),
            1000786: Buff("Battle Litany", 0.1, bonus='crit'),
            1001185: Buff("Brotherhood", 1.05),
            1001825: Buff("Devilment", 0.2, bonus='critdirect'),
            1001878: Buff("Divination", 1.06),
            1002105: Buff("Standard Finish", 1.05),
            1001822: Buff("Technical Finish", 1.05),
            1003889: Buff("The Spear", 1.06),
            1001221: Buff("Chain Stratagem", 0.1, bonus='crit', target=True),
            1002198: Buff("Vulnerability Down", target=True),
            1003849: Buff("Dokumori", 1.05, target=True)
        }

        def get_fru_void(fight):
            ''''''
            enemies = fight.enemy_npcs()
            for enemy in enemies:
                if enemy.game_id == 17828:
            return enemy.id


class Pictomancer:
    def __init__(self, int_stat=0, crit_stat=0, dh_stat=0, det_stat=0):
        
        self.int = int_stat
        self.crit = crit_stat
        self.dh = dh_stat
        self.det = det_stat

        # name, pot, dot?, c/d/cd?, cleave % (0 is aoe)
        self.skills = {          
            34651: Attack("Aero in Green", 530),
            34653: Attack("Blizzard in Cyan", 860),
            34672: Attack("Clawed Muse", 800, cleave=0.7),
            34663: Attack("Comet in Black", 940, cleave=0.65),
            34673: Attack("Fanged Muse", 800, cleave=0.7),
            34650: Attack("Fire in Red", 490),
            34679: Attack("Hammer Brush", 580, cd='CD', cleave=0.7),
            34678: Attack("Hammer Stamp", 560, cd='CD', cleave=0.7),
            34662: Attack("Holy in White", 570, cleave=0.65),
            34676: Attack("Mog of the Ages", 1000, cleave=0.7),
            34680: Attack("Polishing Hammer", 600, cd='CD', cleave=0.7),
            34670: Attack("Pom Muse", 800, cleave=0.7),
            34688: Attack("Rainbow Drip", 1000, cleave=0.85),
            34677: Attack("Retribution of the Madeen", 1100, cleave=0.7),
            34681: Attack("Star Prism", 1100, cleave=0.7),
            34654: Attack("Stone in Yellow", 900),
            34655: Attack("Thunder in Magenta", 940),
            34652: Attack("Water in Blue", 570),
            34671: Attack("Winged Muse", 800),
            7: Attack("Attack", 1)
        }

        self.buffs = [1003685]
