from colorama import Fore, Style
import random
import time
from inventory import Inventory
from items import *
from attack import calculate_attack
from item_data import *
from text_utils import *

class Player:
    def __init__(self, name, hp, strength, speed, intelligence, defense, money, weapon=None):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.speed = speed
        self.intelligence = intelligence
        self.defense = defense
        self.money = money
        self.max_hp = self.hp
        self.weapon = weapon
        self.xp = 0
        self.level = 1
        self.status_effects = []
        self.inventory = Inventory() 

    def punch(self, enemy):
        # Punch uses base strength and weapon damage isn't factored in
        if random.random() < 0.15:  # Miss chance
            print(Fore.YELLOW + self.name + " swings at " + enemy.name + " but misses!" + Fore.WHITE)
            print("")
            smart_sleep(1)
            return
        # Calculate damage with a small variation
        raw_damage = calculate_attack(self.strength)
        damage = max(1, raw_damage - enemy.defense)
    
        enemy.hp -= damage
        print(self.name + " punches " + enemy.name + " for " + str(damage) + " damage!")
        if enemy.defense > 0:
            print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
        print("")
        print(enemy.name + " remaining HP: " + str(enemy.hp))
        print("")

    def attack(self, enemy):
        # Check for miss chance
        if random.random() < 0.15:
            print(Fore.YELLOW + self.name + " swings at " + enemy.name + " but misses!" + Fore.WHITE)
            print("")
            smart_sleep(1)
            return
        raw_damage = calculate_attack(self.strength, self.weapon.damage if self.weapon else 0)
        damage = max(1, raw_damage - enemy.defense)
        enemy.hp -= damage
        print(self.name + " attacks " + enemy.name + " with " + (self.weapon.name if self.weapon else 'bare hands') + " for " + str(damage) + " damage!")
        if enemy.defense > 0:
            print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
            print("")
        print("")
        print(enemy.name + " remaining HP: " + str(enemy.hp))
        print("")
        smart_sleep(1)

    
    def show_inventory(self):
        self.inventory.show_inventory()
    
    def use_item(self, index, target=None):
        self.inventory.use_item(self, index, target)

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(self.weapon, "equipped.")

    def unequip_weapon(self):
        self.weapon = None  
        print("Weapon unequipped.")

    def level_up(self):
        level_thresholds = {
            2: 100,
            3: 300,
            4: 600,
            5: 1000,
            6: 1500,
            7: 2100,
            8: 2800,
            9: 3700,
            10: 4800,
            11: 6200,
            12: 7900,
            13: 10000,
            14: 12400,
            15: 15500,
            16: 19400,
            17: 24200,
            18: 30000,
            19: 37000,
            20: 45500,
            21: 55600,
            22: 67600,
            23: 81800,
            24: 98400,
            25: 118500,
            26: 142500,
            27: 171000,
            28: 204000,
            29: 242000,
            30: 286000,
            31: 336000,
            32: 392000,
            33: 455000,
            34: 525000,
            35: 602000,
            36: 687000,
            37: 780000,
            38: 880000,
            39: 988000,
            40: 1100000,
            41: 1235000,
            42: 1385000,
            43: 1550000,
            44: 1730000,
            45: 1925000,
            46: 2135000,
            47: 2360000,
            48: 2600000,
            49: 2855000,
            50: 3125000,
            51: 3410000,
            52: 3710000,
            53: 4025000,
            54: 4355000,
            55: 4700000,
            56: 5060000,
            57: 5435000,
            58: 5825000,
            59: 6230000,
            60: 6650000,
            61: 7085000,
            62: 7535000,
            63: 8000000,
            64: 8480000,
            65: 8975000,
            66: 9485000,
            67: 10000000,
            68: 10550000,
            69: 11130000,
            70: 11750000,
            71: 12400000,
            72: 13080000,
            73: 13790000,
            74: 14540000,
            75: 15320000,
            76: 16130000,
            77: 16980000,
            78: 17860000,
            79: 18770000,
            80: 19710000,
            81: 20680000,
            82: 21680000,
            83: 22710000,
            84: 23770000,
            85: 24860000,
            86: 25980000,
            87: 27130000,
            88: 28310000,
            89: 29520000,
            90: 30760000,
            91: 32030000,
            92: 33330000,
            93: 34660000,
            94: 36020000,
            95: 37410000,
            96: 38830000,
            97: 40280000,
            98: 41760000,
            99: 43270000,
            100: 44810000
        }


        while self.level + 1 in level_thresholds and self.xp >= level_thresholds[self.level + 1]:
            self.level += 1
            self.max_hp += 10
            self.hp = self.max_hp
            self.strength += 2
            self.defense += 1
            self.intelligence += 1

            typewriter("")
            typewriter(center_text(Fore.MAGENTA + "LEVEL UP!" + Style.RESET_ALL))
            typewriter(center_text("You are now level " + str(self.level) + "!"))
            typewriter(center_text("HP: " + str(self.max_hp)))
            typewriter(center_text("Strength: " + str(self.strength)))
            typewriter(center_text("Defense: " + str(self.defense)))
            typewriter(center_text("Intelligence: " + str(self.intelligence)))
            typewriter("")

            input(center_text("Press Enter to continue..."))

    def apply_status(self, effect, duration):
        self.status_effects.append({'effect': effect, 'duration': duration})
        typewriter(self.name + " is affected by " + effect + " for " + str(duration) + " turn(s).")

    def remove_status(self, effect, duration):
        self.status_effects = [se for se in self.status_effects if se['effect'] != effect]
    
    def process_status_effects(self):
        updated_effects = []
        for effect in self.status_effects:
            effect['duration'] -= 1

            if effect['effect'] == 'stagger':
                self.speed = max(1, self.speed - 2)
                if effect['duration'] <= 0:
                    self.speed += 2
                else:
                    updated_effects.append(effect)

            elif effect['effect'] == 'defending':
                if effect['duration'] <= 0:
                    self.defense -= effect['boost']
                    typewriter(Fore.BLUE + self.name + "'s defense boost has faded." + Fore.RESET)
                else:
                    updated_effects.append(effect)

            else:
                if effect['duration'] > 0:
                    updated_effects.append(effect)

        self.status_effects = updated_effects

    def is_staggered(self):
        return any(se['effect'] == 'stagger' for se in self.status_effects)
    
    def defend(self):
        for effect in self.status_effects:
            if effect['effect'] == 'defending':
                effect['duration'] = random.randint(3, 5)
                typewriter(Fore.CYAN + self.name + " refreshes their defensive stance!" + Fore.RESET)
                print("")
                return

        duration = random.randint(3, 5)
        percent_increase = max(1, int(self.defense * 0.1))
        level_bonus = self.level
        defense_boost = percent_increase + level_bonus

        self.defense += defense_boost
        self.status_effects.append({'effect': 'defending', 'duration': duration, 'boost': defense_boost})

        typewriter(Fore.BLUE + self.name + " braces for impact, raising defense by " +
                str(defense_boost) + " for " + str(duration) + " turns!" + Fore.RESET)
        print("")