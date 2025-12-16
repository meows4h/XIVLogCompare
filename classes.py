import math
from fflogsapi import GQLEnum
from utilities import add_space, milli_to_clock

# instance holds the fight reports + does the comparing functions
# fights hold players and report information
# players hold jobs and base information
# jobs hold attack and buff information
# attacks hold potency, cleave, etc
# buffs hold percentage, type, etc
class Fight:
    def __init__(self, report, p_name, code, num):
        self.report = report
        self.duration = report.duration()
        self.name = report.encounter().name()
        self.player = self.get_player(p_name)
        self.events = self.get_events("DamageDone")
        self.id = code
        self.num = num

        self.void_ids = []
        if self.name == "Futures Rewritten":
            self.void_ids.append(self.get_fru_void())

        self.damage, self.casts = self.get_attacks()

    def get_player(self, name):
        ''''''
        for player in self.report.player_details():
            if player.name == name:
                job = self.get_job(player.job.name)
                player_out = Player(player.id, job, name)
                return player_out

    def get_events(self, cat):
        ''''''
        events = self.report.events({"dataType": GQLEnum(cat),
                                     "sourceID": self.player.pid})
        return events
    
    def get_job(self, job_name):
        ''''''
        if job_name == "Pictomancer":
            return Pictomancer()
        else:
            return None

    def get_fru_void(self):
        ''''''
        enemies = self.report.enemy_npcs()
        for enemy in enemies:
            if enemy.game_id == 17828:
                return enemy.id
            
    def get_attacks(self):
        ''''''
        dmg_events = []
        dmg_count = {}
        for event in self.events:
            if "abilityGameID" in event and event["type"] == "damage":

                if event["targetID"] in self.void_ids:
                    continue

                dmg_events.append(event)
                cid = event["abilityGameID"]
                if cid in self.player.job.skills:
                    cast_name = self.player.job.skills[cid].name
                    if cast_name in dmg_count:
                        dmg_count[cast_name][0] += 1
                        dmg_count[cast_name][1] += event["amount"]
                    else:
                        dmg_count[cast_name] = [1, event["amount"]]

        return dmg_events, dmg_count


class Attack:
    def __init__(self, name, pot, dot=False, cd=None, cleave=1, gcd=True):
        self.name = name
        self.potency = pot
        self.dot = dot
        self.cd = cd
        self.cleave = cleave
        self.gcd = gcd

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
    def __init__(self, pid, job, name):
        self.pid = pid
        self.job = job
        self.name = name


class Instance:
    def __init__(self):
        self.fights = []

        self.buffs = {
            1002599: Buff("Arcane Circle", 1.03),
            1002218: Buff("Army's Paeon", 0.03, bonus='direct'),
            1000141: Buff("Battle Voice", 0.20, bonus='direct'),
            1002217: Buff("Mage's Ballad", 1.01),
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
            1002198: Buff("Vulnerability Down", 1.00, target=True),
            1003849: Buff("Dokumori", 1.05, target=True)
        }

    def set_pids(self, pids):
        ''''''
        for pid in pids:
            self.players.append(Player(pid))

    def add_fight(self, fight):
        ''''''
        self.fights.append(fight)

    def print_compare(self):
        ''''''
        main_job = self.fights[0].player.job
        output = {}
        
        gcds = {}
        for fight in self.fights:
            gcds[f"{fight.id}{fight.num}"] = 0

        for cid in main_job.skills:
            attack = main_job.skills[cid].name
            gcd = main_job.skills[cid].gcd
            output[attack] = []

            for fight in self.fights:
                if attack in fight.casts:
                    output[attack].append(fight.casts[attack])
                    if gcd:
                        gcds[f"{fight.id}{fight.num}"] += fight.casts[attack][0]
                else:
                    output[attack].append([0, 0])
        
        print(f"{add_space(length=27)}", end='')
        for fight in self.fights:
            clock = milli_to_clock(fight.duration)
            print(f"{add_space(f'{fight.player.name} ({clock})', 34)}", end='')
        print("")

        for cast in output:
            base_casts = 0
            base_dmg = 0
            for idx, amt in enumerate(output[cast]):
                if idx == 0:
                    base_casts = amt[0]
                    base_dmg = amt[1]

                    name_print = add_space(cast, 25)
                    base_print = add_space(f'{base_casts} ({base_dmg})', 30)

                    print(f"{name_print}: {base_print} | ", end="")
                else:
                    diff_casts = amt[0] - base_casts
                    diff_dmg = amt[1] - base_dmg

                    cast_print = add_space(f"{amt[0]} ({amt[1]})", 15)
                    diff_print = add_space(f"[{diff_casts} ({(diff_dmg)})]", 15)

                    print(f"{cast_print} {diff_print} | ", end="")
            print("")

        print(f"{add_space('GCDs:', 27)}", end="")
        for fight in self.fights:
            
            print(f"{add_space(f'{gcds[f'{fight.id}{fight.num}']}', 34)}", end="")


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
            34672: Attack("Clawed Muse", 800, cleave=0.7, gcd=False),
            34663: Attack("Comet in Black", 940, cleave=0.65),
            34673: Attack("Fanged Muse", 800, cleave=0.7, gcd=False),
            34650: Attack("Fire in Red", 490),
            34679: Attack("Hammer Brush", 580, cd='CD', cleave=0.7),
            34678: Attack("Hammer Stamp", 560, cd='CD', cleave=0.7),
            34662: Attack("Holy in White", 570, cleave=0.65),
            34676: Attack("Mog of the Ages", 1000, cleave=0.7, gcd=False),
            34680: Attack("Polishing Hammer", 600, cd='CD', cleave=0.7),
            34670: Attack("Pom Muse", 800, cleave=0.7, gcd=False),
            34688: Attack("Rainbow Drip", 1000, cleave=0.85),
            34677: Attack("Retribution of the Madeen", 1100, cleave=0.7, gcd=False),
            34681: Attack("Star Prism", 1100, cleave=0.7),
            34654: Attack("Stone in Yellow", 900),
            34655: Attack("Thunder in Magenta", 940),
            34652: Attack("Water in Blue", 570),
            34671: Attack("Winged Muse", 800, gcd=False),
            7: Attack("Attack", 1, gcd=False)
        }

        self.buffs = [1003685]
