from colorama import Fore, Style
import random
import math
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
        strength_variation = random.randint(-1, 1)
        raw_damage = self.strength + strength_variation
        damage = max(1, raw_damage - enemy.defense)
    
        enemy.hp -= damage
        print(self.name + " punches " + enemy.name + " for " + str(damage) + " damage!")
        print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
        print("")
        print(enemy.name + " remaining HP: " + str(enemy.hp))
        print("")


    def attack(self, enemy):
        raw_damage = calculate_attack(self.strength, self.weapon.damage if self.weapon else 0)
        damage = max(1, raw_damage - enemy.defense)
        enemy.hp -= damage
        print(self.name + " attacks " + enemy.name + " with " + (self.weapon.name if self.weapon else 'bare hands') + " for " + str(damage) + " damage!")
        print(Fore.LIGHTBLACK_EX + "(Reduced from " + str(raw_damage) + " by defense)" + Fore.WHITE)
        print("")
        print(enemy.name + " remaining HP: " + str(enemy.hp))
        print("")
        time.sleep(1)
    
    def show_inventory(self):
        self.inventory.show_inventory()
    
    def use_item(self, index, target=None):
        self.inventory.use_item(self, index, target)

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(self.weapon,"equipped.")

    def unequip_weapon(self):
        self.weapon = None  
        print("Weapon unequipped.")

    def level_up(self):
        level_thresholds = {
            2: 100,
            3: 250,
            4: 450,
            5: 700,
            6: 1000,
            7: 1350,
            8: 1750,
            9: 2200,
            10: 2700
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


    def apply_status(self,effect,duration):
        self.status_effects.append({'effect': effect, 'duration': duration})
        typewriter(self.name + " is affected by " + effect + " for " + str(duration) + " turn(s).")

    def remove_status(self,effect,duration):
        self.status_effects = [se for se in self.status_effects if se['effect'] != effect]
    
    def process_status_effects(self):
        for effect in self.status_effects:
            if effect['effect'] == 'stagger':
                self.speed = max(1, self.speed - 2) 
                effect['duration'] -= 1
                if effect['duration'] <= 0:
                    self.remove_status('stagger')
                    self.speed += 2 

    def is_staggered(self):
        return any(se['effect'] == 'stagger' for se in self.status_effects)